// Parents have children
// Children have kittens (obviously)

function createParent(id) {
    id = id + 1;
    return {
        'name': 'parent ' + id,
        'id': id,
        '_type': 'parent'
    };
}

function createChild(id, parent) {
    id = id + 1;
    return {
        'id': id,
        'name': 'child ' + id,
        'parent_id': parent.id,
        '_type': 'child'
    };
}

function createKitten(id, child) {
    id = id + 1;
    return {
        'id': id,
        'name': 'kitten ' + id,
        'child_id': child.id,
        '_type': 'kitten'
    };
}

function generateParentsAndChildren() {
    var parents = [];
    var lastChildId = 0;
    var lastKittenId = 0;
    for (var i = 0; i < 5; i++) {
        var parent = createParent(i)
        parent.children = []
        for (var j = 0; j < 4; j++) {
            var child = createChild(lastChildId, parent);
            child.kittens = []
            for (x = 0; x < 2; x++) {
                child.kittens.push(createKitten(lastKittenId, child));
                lastKittenId++;
            }
            parent.children.push(child);
            lastChildId++;
        }
        parents.push(parent);
    }
    return parents;
}

function generateFooBar() {
    return {
        name: 'foo',
        id: 1,
        _type: 'foo',
        bar: {
            name: 'bar',
            id: 1,
            _type: 'bar',
            foo_id: 1
        }
    }
}


function createStaff(id) {
    return {
        _type: 'staff',
        id: id,
        documents: []
    }
}

function createDocument(id, staff_ids) {
    return {
        _type: 'document',
        content: 'document ' + id,
        id: id,
        staff_id: staff_ids
    }
}

function generateStaffDocuments() {
    var staff = []

    for (var i = 1; i < 4; i++) {
        var documents = []
        for (var j = 1; j < 4; j++) {
            var doc = createDocument(j, [1, 2, 3]);
            documents.push(doc);
        }

        var staffMember = createStaff(i);
        staffMember.documents = documents;
        staff.push(staffMember);
    }
    return staff;
}


function aatestMapper() {
    return [
        {
            "parent_type": "company",
            "via": "company_id",
            "prop_name": "staff",
            "child_type": "staff",
            "is_collection": true
        },
        {
            "parent_type": "staff",
            "via": "staff_id",
            "prop_name": "documents",
            "child_type": "document",
            "is_collection": true
        },
        {
            "parent_type": "document",
            "via": "document_id",
            "prop_name": "staff",
            "child_type": "staff",
            "is_collection": false
        },
        {
            "parent_type": "company",
            "via": "company_id",
            "prop_name": "companyowner",
            "child_type": "companyowner",
            "is_collection": true
        }
    ];
}

function aadataPackage() {
    return [
        {
            "staff": [
                {
                    "documents": [
                        {
                            "staff": null,
                            "content": "hello world",
                            "title": "test",
                            "id": 1,
                            "$$hashKey": "008"
                        }
                    ],
                    "company_id": 1,
                    "id": 1,
                    "name": "hila",
                    "$$hashKey": "006"
                }
            ],
            "companyowner": {
                "company_id": null,
                "id": null,
                "name": ""
            },
            "name": "test",
            "id": 1,
            "$$hashKey": "004"
        }
    ]
}

function aadataSource() {
    return {
        "action": "updated",
        "data": {
            "name": "ahila",
            "documents": [
                {
                    "staff": null,
                    "content": "hello world",
                    "id": 1,
                    "title": "test"
                }
            ],
            "company_id": 1,
            "id": 1
        }
    }
}