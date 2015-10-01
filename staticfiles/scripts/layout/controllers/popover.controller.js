'use strict';

	angular.module('minovateApp') 

.controller('PopoverCtrl', function ($scope) {
    vm.dynamicPopover = {
        content: 'Hello, World!',
        templateUrl: 'myPopoverTemplate.html',
        title: 'Title'

    };
});