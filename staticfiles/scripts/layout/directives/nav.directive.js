(function () {
  'use strict';

  angular
    .module('layout.directives')
    .directive('navItems', navItems);

  function navItems() {

	var directive = {
  		replace: true,
  		transclude:true,
  		restrict: 'E',
      scope: true,
      template:
        '<li>'+
           '<a href="javascript:;"><fa name="{{vm.icon[$index]}}"></fa> <span>{{domain}}</span></a>'+
           '<ul>'+
               '<li ui-sref-active="active" class="dropdown submenu" ng-repeat="(fam, v) in value | groupBy: \'family\' | orderBy:\'id\'" >'+
               '<a href="javascript:;"><fa name="caret-right"></fa><span>{{fam}}</span><i class="fa fa-plus"></i></a>'+
                   '<ul>'+
                       '<li ui-sref-active="active" class="dropdown submenu" ng-repeat="sf in v"><a ui-sref="app.orders.request({goodId:sf.id})">{{sf.subfamily}}</a></li>'+
                   '</ul>'+
               '</li>'+
           '</ul>'+
         '</li>',
      link: function($scope, $el, attrs) {
          var $dropdowns = $el.find('ul').parent('li'),
              $a = $dropdowns.children('a'),
              $notDropdowns = $el.children('li').not($dropdowns),
              $notDropdownsLinks = $notDropdowns.children('a'),
              app = angular.element('#minovate'),
              sidebar = angular.element('#sidebar'),
              controls = angular.element('#controls');

          $dropdowns.addClass('dropdown');

          var $submenus = $dropdowns.find('ul >.dropdown');
          $submenus.addClass('submenu');

          $a.append('<i class="fa fa-plus"></i>');

          $a.on('click', function(event) {
            if (app.hasClass('sidebar-sm') || app.hasClass('sidebar-xs') || app.hasClass('hz-menu')) {
              return false;
            }

            var $this = angular.element(this),
                $parent = $this.parent('li'),
                $openSubmenu = angular.element('.submenu.open');

            if (!$parent.hasClass('submenu')) {
              $dropdowns.not($parent).removeClass('open').find('ul').slideUp();
            }

            $openSubmenu.not($this.parents('.submenu')).removeClass('open').find('ul').slideUp();
            $parent.toggleClass('open').find('>ul').stop().slideToggle();
            event.preventDefault();
          });

          $dropdowns.on('mouseenter', function() {
            sidebar.addClass('dropdown-open');
            controls.addClass('dropdown-open');
          });

          $dropdowns.on('mouseleave', function() {
            sidebar.removeClass('dropdown-open');
            controls.removeClass('dropdown-open');
          });

          $notDropdownsLinks.on('click', function() {
            $dropdowns.removeClass('open').find('ul').slideUp();
          });

          var $activeDropdown = angular.element('.dropdown>ul>.active').parent();

          $activeDropdown.css('display', 'block');
        },
	}

    return directive;
  }

})();