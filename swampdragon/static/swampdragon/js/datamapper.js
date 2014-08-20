// indexOf from http://stackoverflow.com/questions/1181575/javascript-determine-whether-an-array-contains-a-value
var indexOf = function (needle) {
    if (typeof Array.prototype.indexOf === 'function') {
        indexOf = Array.prototype.indexOf;
    } else {
        indexOf = function (needle) {
            var i = -1, index = -1;

            for (i = 0; i < this.length; i++) {
                if (this[i] === needle) {
                    index = i;
                    break;
                }
            }

            return index;
        };
    }

    return indexOf.call(this, needle);
};

var DataMapper = function (channelMaps) {
    var dataMapper = this;
    dataMapper.channelMaps = channelMaps;

    dataMapper.mapData = function (datasource, message) {
        if (message.action == "created") {
            dataMapper.mapCreated(datasource, message.data);
        }
        else if (message.action == "updated") {
            dataMapper.mapUpdated(datasource, message.data);
        }
        else if (message.action == "deleted") {
            dataMapper.mapDelete(datasource, message.data);
        }
    };

    dataMapper.mapCreated = function (datasource, data) {
        var channelMap = dataMapper._findMapping(data._type);

        // Don't add an instance that already exists
        var instance = dataMapper._findByIdAndType(datasource, data.id, data._type);
        if (instance.length > 0) {
            return datasource;
        }

        var parents = [];
        if (channelMap != null) {
            parents = dataMapper._findByIdAndType(datasource, data[channelMap.via], channelMap.parent_type);
        }

        if (parents.length > 0) {
            for (var i in parents) {
                var parent = parents[i];
                if (channelMap.is_collection) {
                    parent[channelMap['prop_name']].push(data);
                } else {
                    parent[channelMap['prop_name']] = data;
                }
            }
        }
        else if (channelMap == null) {
            if (datasource instanceof Array)
                datasource.push(data);
            else
                datasource = data;
        }

        return datasource;
    };

    dataMapper.mapUpdated = function(datasource, data) {
        var channelMap = dataMapper._findMapping(data._type);
        var instances = dataMapper._findByIdAndType(datasource, data.id, data._type);
        for (var i in instances) {
            var instance = instances[i];
            if (instance != null) {
                for (var key in data) {
                    instance[key] = data[key];
                }
            }
        }
        var removedChildren = dataMapper._removeOldParents(datasource, data, channelMap);
        if (removedChildren.length == 0) {
            dataMapper._attachToParents(datasource, data, channelMap);
        }
        for (var c in removedChildren) {
            dataMapper._attachToParents(datasource, removedChildren[c], channelMap);
        }

        if (instances.length == 0 && channelMap == null) {
            if (datasource instanceof Array) {
                datasource.push(data);
            } else {
                datasource = data;
            }
        }
        return datasource;
    };

    dataMapper.mapDelete = function(datasource, data) {
        var channelMap = dataMapper._findMapping(data._type);
        var parents = dataMapper._findCurrentParents(datasource, data, channelMap);
        for (var p in parents) {
            var parent = parents[p];
            var children = parent[channelMap.prop_name];
            if (children instanceof Array) {
                for (var i in children) {
                    if (dataMapper._compareIds(children[i].id, data.id)) {
                        parent[channelMap.prop_name].splice(i, 1);
                    }
                }
            } else {
                parent[channelMap.prop_name] = null;
            }
        }

        if (parents.length == 0) {
            if (datasource instanceof Array) {
                for (var i in datasource) {
                    if (dataMapper._compareIds(datasource[i].id, data.id)) {
                        datasource.splice(i, 1);
                    }
                }
            } else {
                if (dataMapper._compareIds(datasource.id, data.id)) {
                    datasource = null;
                }
            }
        }
    };

    // Private helper functions
    // ------------------------
    dataMapper._findMapping = function (dataType) {
        if (dataMapper.channelMaps == null) {
            return null;
        }

        for (var i in dataMapper.channelMaps) {
            var dataMap = dataMapper.channelMaps[i];
            if (dataMap.child_type == dataType) {
                return dataMap;
            }
        }
        return null;
    };

    dataMapper._findByIdAndType = function (datasource, id, dataType, result) {
        if (result == null)
            result = [];

        function find(entry) {
            if (entry._type == dataType) {
                if (dataMapper._compareIds(entry.id, id)) {
                    result.push(entry);
                }
            } else {
                for (var prop in entry) {
                    if (entry[prop] instanceof Object) {
                        dataMapper._findByIdAndType(entry[prop], id, dataType, result);
                    }
                }
            }
        }

        if (datasource instanceof Array) {
            for (var i in datasource) {
                find(datasource[i]);
            }
        } else {
            find(datasource);
        }

        return result;
    };

    dataMapper._findCurrentParents = function (datasource, data, channelMap, result) {
        if (result == null)
            result = [];
        if (channelMap == null)
            channelMap = dataMapper._findMapping(data._type);
        if (channelMap == null) {
            return result;
        }

        if (!(datasource instanceof Array)) {
            if (datasource._type == channelMap.parent_type) {
                if (dataMapper._compareIds(datasource.id, data[channelMap.via])) {
                    result.push(datasource);
                }
            }
        } else {
            for (var i in datasource) {
                var entry = datasource[i];
                if (entry._type == channelMap.parent_type) {
                    if (channelMap.is_collection) {
                        for (var p in entry[channelMap.prop_name]) {
                            if (dataMapper._compareIds(entry[channelMap.prop_name][p].id, data.id)) {
                                result.push(entry);
                            }
                        }
                    } else {
                        if (entry[channelMap.prop_name] != null && dataMapper._compareIds(entry[channelMap.prop_name].id, data.id)) {
                            result.push(entry);
                        }
                    }
                } else {
                    for (var prop in entry) {
                        if (entry[prop] instanceof Object) {
                            this._findCurrentParents(entry[prop], data, channelMap, result);
                        }
                    }
                }
            }
        }

        return result;
    };

    dataMapper._removeOldParents = function (datasource, data, channelMap, result) {
        var poppedChildren = [];
        var parents = dataMapper._findCurrentParents(datasource, data, channelMap);
        for (var p in parents) {
            var parent = parents[p];
            if (dataMapper._compareIds(parent.id, data[channelMap.via]) == false) {
                var children = parent[channelMap.prop_name];
                if (channelMap.is_collection) {
                    for (var c in children) {
                        var child = children[c];
                        if (dataMapper._compareIds(child.id, data.id)) {
                            poppedChildren.push(children.splice(c, 1)[0]);
                        }
                    }
                } else {
                    parent[channelMap.prop_name] = null;
                }
            }
        }
        return poppedChildren;
    };

    dataMapper._attachToParents = function (datasource, data, channelMap) {
        if (channelMap == null)
            return;
        var parentIds = data[channelMap.via];
        var parents = [];
        if (parentIds instanceof Array) {
            for (var pid in parentIds) {
                var parentId = parentIds[pid];
                var parentList = dataMapper._findByIdAndType(datasource, parentId, channelMap.parent_type);
                for (var p in parentList)
                    parents.push(parentList[p]);
            }
        } else {
            parents = dataMapper._findByIdAndType(datasource, parentIds, channelMap.parent_type);
        }

        for (var i in parents) {
            var shouldAdd = true;
            var parent = parents[i];

            if (channelMap.is_collection) {
                for (var c in parent[channelMap.prop_name]) {
                    var child = parent[channelMap.prop_name][c];
                    if (dataMapper._compareIds(child.id, data.id)) {
                        shouldAdd = false;
                        break;
                    }
                }
                if (shouldAdd) {
                    parent[channelMap.prop_name].push(data);
                }
            } else {
                parent[channelMap.prop_name] = data;
            }
        }
    };

    dataMapper._compareIds = function(idA, idB) {
        if (idB == null || idA == null) {
            return false;
        }
        if (idB instanceof Array) {
            for (var i in idB) {
                if (idB[i].toString() == idA) {
                    return true;
                }
            }
            return false;
        } else {
            return idA.toString() == idB.toString();
        }
    };

    return dataMapper;
};
