findModel = function(datasource, data) {
    return datasource[1];
};

updateData = function($scope, data) {
    var parent = findModel($scope.datasource, data);
    var child = parent.children[0];
//    var child = $scope.datasource[1].children[0]
    child.name = "child 1 updated";
};


describe('PhoneListCtrl', function () {
    it('should update a child', function () {
        var $scope = {};
        $scope.channelMaps = [
            {'type': 'child', map_from: 'parent_id', map_to: 'children' },
            {'type': 'subchild', map_from: 'child_id', map_to: 'children' }
        ];
        $scope.datasource = [];
        $scope.datasource.push({
            parent: 'test parent 1',
            id: 1
        });
        $scope.datasource.push({
            parent: 'test parent 2',
            id: 2,
            children: [
                {_type: "child", id:1, parent_id: 2, name: "child 1"},
                {_type: "child", id:2, parent_id: 2, name: "child 2"}
            ]
        });
        $scope.datasource.push({
            parent: 'test parent 3',
            id: 3
        });

        data = {_type: "child", id:1, parent_id: 2, name: "child 1 updated"};
        updateData($scope, data);

        expect($scope.datasource[1].children[0].name).toBe("child 1 updated");
    });
});
