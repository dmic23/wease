'use strict';

/**
 * @ngdoc function
 * @name minovateApp.controller:FormUploadCtrl
 * @description
 * # FormUploadCtrl
 * Controller of the minovateApp
 */
angular.module('minovateApp')
  .controller('FormUploadCtrl', ['$scope', '$cookies', 'FileUploader', 'Requests', function($scope, $cookies, FileUploader, Requests) {
    
    var vm = this;

    var csrf_token = $cookies.csrftoken;
    
    var uploader = $scope.uploader = new FileUploader({
      // method: 'POST',
      // url: '/api/v1/req-items/'+reqItem+'/req-files/',
      url: static_path('scripts/modules/fileupload/upload.php')
      // headers : {
      //   'X-CSRFToken': csrf_token 
      // },
     
    });

    console.log(Requests);
    // console.log($scope.reqId);
    console.log(vm.reqId);
    // FILTERS

    uploader.filters.push({
      name: 'customFilter',
      fn: function() {
        return this.queue.length < 10;
      }
    });
    console.log(uploader);
    // CALLBACKS

    uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
      console.info('onWhenAddingFileFailed', item, filter, options);
    };
    uploader.onAfterAddingFile = function(fileItem) {
      console.info('onAfterAddingFile', fileItem);
    };
    uploader.onAfterAddingAll = function(addedFileItems) {
      console.info('onAfterAddingAll', addedFileItems);
    };
    uploader.onBeforeUploadItem = function(item) {
      console.info('onBeforeUploadItem', item);
    };
    uploader.onProgressItem = function(fileItem, progress) {
      console.info('onProgressItem', fileItem, progress);
    };
    uploader.onProgressAll = function(progress) {
      console.info('onProgressAll', progress);
    };
    uploader.onSuccessItem = function(fileItem, response, status, headers) {
      console.info('onSuccessItem', fileItem, response, status, headers);
    };
    uploader.onErrorItem = function(fileItem, response, status, headers) {
      console.info('onErrorItem', fileItem, response, status, headers);
    };
    uploader.onCancelItem = function(fileItem, response, status, headers) {
      console.info('onCancelItem', fileItem, response, status, headers);
    };
    uploader.onCompleteItem = function(fileItem, response, status, headers) {
      console.info('onCompleteItem', fileItem, response, status, headers);
      console.log(fileItem.file);

    };
    uploader.onCompleteAll = function() {
      console.info('onCompleteAll');
    };

    console.info('uploader', uploader);
  }]);
