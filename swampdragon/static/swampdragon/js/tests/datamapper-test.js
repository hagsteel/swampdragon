var parentChildrenMaps = [{
    parent_type: 'parent',
    child_type: 'child',
    prop_name: 'children',
    is_collection: true,
    via: 'parent_id'
}, {
    parent_type: 'child',
    child_type: 'kitten',
    prop_name: 'kittens',
    is_collection: true,
    via: 'child_id'
}];


var oneToOneMaps = [{
    parent_type: 'foo',
    child_type: 'bar',
    prop_name: 'bar',
    is_collection: false,
    via: 'foo_id'
}];

var staffDocMaps = [{
    parent_type: 'staff',
    child_type: 'document',
    prop_name: 'documents',
    is_collection: true,
    via: 'staff_id'
}];

describe('dataMapper with one to many', function () {
    it('should find parent with id 2', function() {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = generateParentsAndChildren();

        var child = datasource[2].children[1];
        var parents = dataMapper._findCurrentParents(datasource, child);
        expect(parents[0].id).toBe(3);
    });

    it('should find kitten with id 1', function() {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = generateParentsAndChildren();

        var data = {_type: "kitten", id: 12, name: "kitten 100", child_id: 7};
        var kittens = dataMapper._findByIdAndType(datasource, data.id, data._type);
        expect(kittens[0].id).toBe(12);
    });

    it('should add a new parent to a list of parents', function () {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = [];

        var data = {_type: "parent", id: 1, name: "parent 1"};
        datasource = dataMapper.mapCreated(datasource, data);
        expect(datasource[0].name).toBe("parent 1");
    });

    it('should set the datasource to an instance of a parent', function () {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = {};

        var data = {_type: "parent", id: 1, name: "parent 1"};
        datasource = dataMapper.mapCreated(datasource, data);
        expect(datasource.name).toBe("parent 1");
    });

    it('should add a kitten to a child', function () {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = generateParentsAndChildren();

        var data = {_type: "kitten", id: 100, name: "kittie pooh", child_id: 6};
        datasource = dataMapper.mapCreated(datasource, data);
        var child = datasource[1].children[1];
        expect(child.kittens[child.kittens.length -1].name).toBe("kittie pooh");
    });

    it('should update a kitten of a child', function () {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = generateParentsAndChildren();

        var child = datasource[1].children[0];
        var data = {_type: "kitten", id: child.kittens[0].id, name: "updated kittie", child_id: child.id};
        datasource = dataMapper.mapUpdated(datasource, data);
        expect(child.kittens[0].name).toBe("updated kittie");
    });

    it('should move a kitten to another child after updating the child id', function () {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = generateParentsAndChildren();

        var child = datasource[0].children[0];
        var secondChild = datasource[1].children[1];
        var kitten = child.kittens[0];
        kitten.child_id = secondChild.id;
        kitten.name = "updated kittie";
        datasource = dataMapper.mapUpdated(datasource, kitten);
        expect(child.kittens[0].name).not.toBe("updated kittie");
        expect(secondChild.kittens[secondChild.kittens.length - 1].name).toBe("updated kittie");
    });

    it('should delete a kitten', function () {
        var dataMapper = new DataMapper(parentChildrenMaps);
        var datasource = generateParentsAndChildren();

        var child = datasource[1].children[1];
        var kitten = child.kittens[1];
        expect(child.kittens[1]).toBe(kitten);
        datasource = dataMapper.mapDelete(datasource, kitten);
        expect(child.kittens[1]).not.toBe(kitten);
    });
});


describe("DataMapper with one to one", function() {
    it('should find parent of bar', function() {
        var dataMapper = new DataMapper(oneToOneMaps);
        var datasource = generateFooBar();

        var bar = datasource.bar;
        var parents = dataMapper._findCurrentParents(datasource, bar);
        expect(parents[0].id).toBe(1);
    });

    it('should update bar', function() {
        var dataMapper = new DataMapper(oneToOneMaps);
        var datasource = generateFooBar();

        var data = {_type: "bar", id: datasource.bar.id, name: "updated bar", foo_id: datasource.id};
        var parent = dataMapper.mapUpdated(datasource, data);
        expect(datasource.bar.name).toBe('updated bar');
    });

    it('should add bar', function() {
        var dataMapper = new DataMapper(oneToOneMaps);
        var datasource = generateFooBar();
        datasource.bar = null;

        var data = {_type: "bar", id: 999, name: "created bar", foo_id: datasource.id};
        var parent = dataMapper.mapCreated(datasource, data);
        expect(datasource.bar.name).toBe('created bar');
    });

    it('should delete bar', function() {
        var dataMapper = new DataMapper(oneToOneMaps);
        var datasource = generateFooBar();
        var data = {_type: "bar", id: 1, name: "created bar", foo_id: datasource.id};
        dataMapper.mapDelete(datasource, data);
        expect(datasource.bar).toBe(null);
    });
});

describe("DataMapper with many to many", function() {
    it('should update a document on all staff members', function() {
        var dataMapper = new DataMapper(staffDocMaps);
        var datasource = generateStaffDocuments();
        var data = {_type: 'document', id: datasource[0].documents[0].id, content: 'updated', staff_id: [1,2,3]};
        dataMapper.mapUpdated(datasource, data);
        for (var i in datasource) {
            expect(datasource[i].documents[0].content).toBe('updated');
        }
    });

    it('should add a document to the first two staff members', function() {
        var dataMapper = new DataMapper(staffDocMaps);
        var datasource = generateStaffDocuments();
        var data = {_type: 'document', id: 999, content: 'new doc', staff_id: [1,2]};
        dataMapper.mapCreated(datasource, data);

        expect(datasource[0].documents[3].content).toBe('new doc');
        expect(datasource[1].documents[3].content).toBe('new doc');
        expect(datasource[2].documents.length).toBe(3);
    });

    it('should delete a document from all staff members', function() {
        var dataMapper = new DataMapper(staffDocMaps);
        var datasource = generateStaffDocuments();

        expect(datasource[0].documents[0].id).toBe(1);
        expect(datasource[1].documents[0].id).toBe(1);
        expect(datasource[2].documents[0].id).toBe(1);

        var data = {_type: 'document', id: 1};
        dataMapper.mapDelete(datasource, data);

        expect(datasource[0].documents[0].id).toBe(2);
        expect(datasource[1].documents[0].id).toBe(2);
        expect(datasource[2].documents[0].id).toBe(2);
    });
});