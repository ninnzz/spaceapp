'use strict';

describe('Controller: DisasterlistCtrl', function () {

  // load the controller's module
  beforeEach(module('spaceappApp'));

  var DisasterlistCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    DisasterlistCtrl = $controller('DisasterlistCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
