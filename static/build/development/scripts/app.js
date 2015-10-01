'use strict';

angular
  .module('minovateApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngStorage',
    'ngTouch',
    'picardy.fontawesome',
    'ui.bootstrap',
    'ui.router',
    'ui.utils',
    'angular-loading-bar',
    'angular-momentjs',
    'FBAngular',
    'lazyModel',
    'toastr',
    'angularBootstrapNavTree',
    'oc.lazyLoad',
    'ui.select',
    'ui.tree',
    'textAngular',
    'colorpicker.module',
    'angularFileUpload',
    'ngImgCrop',
    'datatables',
    'datatables.bootstrap',
    'datatables.colreorder',
    'datatables.colvis',
    'datatables.tabletools',
    'datatables.scroller',
    'datatables.columnfilter',
    'ui.grid',
    'ui.grid.resizeColumns',
    'ui.grid.edit',
    'ui.grid.moveColumns',
    'ngTable',
    'smart-table',
    'angular-flot',
    'angular-rickshaw',
    'easypiechart',
    'uiGmapgoogle-maps',
    'ui.calendar',
    'angular.filter',
    'localytics.directives',
    'SwampDragonServices',
    'filters', 
    'authentication',
    'layout',
    'accounts',
    'orders',
    'messages',
  ])
  .run(['$rootScope', '$state', '$stateParams', function($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
    $rootScope.$on('$stateChangeSuccess', function(event, toState) {

      event.targetScope.$watch('$viewContentLoaded', function () {

        angular.element('html, body, #content').animate({ scrollTop: 0 }, 200);

        setTimeout(function () {
          angular.element('#wrap').css('visibility','visible');

          if (!angular.element('.dropdown').hasClass('open')) {
            angular.element('.dropdown').find('>ul').slideUp();
          }
        }, 200);
      });
      $rootScope.containerClass = toState.containerClass;
    });
  }])
  .run(['$rootScope', '$state', 'Authentication',function($rootScope, $state, Authentication) {

    $rootScope.$on('$stateChangeStart', function(event, toState, toParams) {
      var requireLogin = toState.data.requireLogin;
      var auth = Authentication.isAuthenticated();

      if (requireLogin && !auth) {
        event.preventDefault();
        $state.go('core.login');
        return $rootScope;
      }
    });
  }])
  .run(['$http', function ($http){
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';

  }])
  .config(['uiSelectConfig', function (uiSelectConfig) {
    uiSelectConfig.theme = 'bootstrap';
  }])
  .config(function ($urlMatcherFactoryProvider) {
    $urlMatcherFactoryProvider.caseInsensitive(true);
    $urlMatcherFactoryProvider.strictMode(false);
  })
  .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    // $urlRouterProvider.otherwise('/app/dashboard');
    
    $urlRouterProvider.otherwise(function($injector) {
      var $state = $injector.get('$state');
      $state.go('app.dashboard');
    });

    $stateProvider
    //app page
    .state('app', {
      abstract: true,
      url: '/app',
      controller: 'AppController',
      controllerAs: 'vm',     
      templateUrl: static_path('views/tmpl/app.html'),
      data: {
        requireLogin: true
      },
    })
    //dashboard
    .state('app.dashboard', {
      url: '/dashboard',
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: static_path('views/dashboard.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/datatables/datatables.bootstrap.min.css')
          ]);
        }]
      },
      data: {
        requireLogin: true
      },
    })
    // requests/orders/offers
    .state('app.orders', {
      abstract: true,
      url: '/orders',
      template: '<div ui-view></div>'
    })
    // list of all orders
    .state('app.orders.all', {
      url: '/all/{filterParam}',
      params: {
        filterParam: {value: ''}
      },
      controller: 'OrdersController',
      controllerAs: 'vm',
      templateUrl: static_path('views/orders/orders.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/datatables/datatables.bootstrap.min.css'),
            static_path('scripts/vendor/datatables/Pagination/input.js'),
            static_path('scripts/vendor/datatables/ColumnFilter/jquery.dataTables.columnFilter.js')
          ]);
        }],
        allOrders: ['Order',
            function(Order) {
              var ordrs = Order.getAllSimple();
              console.log(ordrs);
            return Order.getAllSimple();
        }],
      }
    })    
    //request
    .state('app.orders.request', {
      url: '/request/:goodId',
      controller: 'RequestController',
      controllerAs: 'vm',
      templateUrl: static_path('views/orders/new-request.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/slider/bootstrap-slider.js'),
            static_path('scripts/vendor/touchspin/jquery.bootstrap-touchspin.js'),
            static_path('scripts/vendor/touchspin/jquery.bootstrap-touchspin.css'),
            static_path('scripts/vendor/filestyle/bootstrap-filestyle.min.js')
          ]);
        }]
      }
    })
    //edit request
    .state('app.orders.edit', {
      url: '/edit/:reqId',
      controller: 'EditRequestController',
      controllerAs: 'vm',
      templateUrl: static_path('views/orders/edit-request.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/slider/bootstrap-slider.js'),
            static_path('scripts/vendor/touchspin/jquery.bootstrap-touchspin.js'),
            static_path('scripts/vendor/touchspin/jquery.bootstrap-touchspin.css'),
            static_path('scripts/vendor/filestyle/bootstrap-filestyle.min.js')
          ]);
        }]
      }
    })
    //add request
    .state('app.orders.add', {
      url: '/:orderId/add/:goodId',
      controller: 'AddRequestController',
      controllerAs: 'vm',
      templateUrl: static_path('views/orders/add-request.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/slider/bootstrap-slider.js'),
            static_path('scripts/vendor/touchspin/jquery.bootstrap-touchspin.js'),
            static_path('scripts/vendor/touchspin/jquery.bootstrap-touchspin.css'),
            static_path('scripts/vendor/filestyle/bootstrap-filestyle.min.js')
          ]);
        }]
      }
    })
    //order
    .state('app.orders.order', {
      url: '/order/:orderId',
      controller: 'OrderController',
      controllerAs: 'vm',
      templateUrl: static_path('views/orders/order.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/datatables/datatables.bootstrap.min.css'),
            static_path('scripts/vendor/datatables/Pagination/input.js'),
            static_path('scripts/vendor/datatables/ColumnFilter/jquery.dataTables.columnFilter.js')
          ]);
        }]
      }
    }) 
    //offer
    .state('app.orders.offer', {
      url: '/offer/:orderId',
      controller: 'OfferController',
      controllerAs: 'vm',
      templateUrl: static_path('views/orders/offer.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/datatables/datatables.bootstrap.min.css'),
            static_path('scripts/vendor/datatables/Pagination/input.js'),
            static_path('scripts/vendor/datatables/ColumnFilter/jquery.dataTables.columnFilter.js')
          ]);
        }]
      }
    })
    //Blank Offer
    .state('app.orders.blankoffer', {
      url: '/blankoffer',
      controller: 'BlankOfferController',
      controllerAs: 'vm',
      templateUrl: static_path('views/orders/offer-blank.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/datatables/datatables.bootstrap.min.css'),
            static_path('scripts/vendor/datatables/Pagination/input.js'),
            static_path('scripts/vendor/datatables/ColumnFilter/jquery.dataTables.columnFilter.js')
          ]);
        }]
      }
    })    
    //example pages
    .state('app.pages', {
      url: '/pages',
      template: '<div ui-view></div>'
    })
    //profile page
    .state('app.pages.profile', {
      url: '/profile/:username',
      controller: 'AccountController',
      controllerAs: 'vm',
      templateUrl: static_path('views/accounts/profile.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/filestyle/bootstrap-filestyle.min.js')
          ]);
        }]
      }
    })
    .state('app.pages.company-profile', {
      url: '/company/:companyId',
      controller: 'CompanySettingsController',
      controllerAs: 'vm',
      templateUrl: static_path('views/accounts/company-profile.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/filestyle/bootstrap-filestyle.min.js')
          ]);
        }]
      }
    })
    .state('app.pages.company-create', {
      url: '/create/company',
      controller: 'CreateCompanyController',
      controllerAs: 'vm',
      templateUrl: static_path('views/accounts/company-create.html'),
      resolve: {
        plugins: ['$ocLazyLoad', function($ocLazyLoad) {
          return $ocLazyLoad.load([
            static_path('scripts/vendor/filestyle/bootstrap-filestyle.min.js')
          ]);
        }]
      }
    })
    //mail
    .state('app.mail', {
      // abstract: true,
      url: '/mail',
      controller: 'MailController',
      controllerAs: 'vm',      
      templateUrl: static_path('views/messages/mail.html'),
    })
    //mail/inbox
    .state('app.mail.inbox', {
      url: '/inbox/{filterParam}',
      params: {
        filterParam: {value: ''}
      },
      controller: 'InboxController',
      controllerAs: 'vm',
      templateUrl: static_path('views/messages/inbox.html')
    })
    //mail/compose
    .state('app.mail.compose', {
      url: '/compose/{filterParam}',
      params: {
        filterParam: {value: ''}
      },
      controller: 'MailComposeController',
      controllerAs: 'vm',
      templateUrl: static_path('views/messages/mail-compose.html')
    })
    //mail/single
    .state('app.mail.single', {
      url: '/single/:mailId',
      controller: 'MailSingleController',
      controllerAs: 'vm',
      templateUrl: static_path('views/messages/mail-single.html')
    })
    //app core pages (errors, login,signup)
    .state('core', {
      abstract: true,
      url: '/core',
      template: '<div ui-view></div>',
      data: {
        requireLogin: false
      }
    })
    //login
    .state('core.login', {
      url: '/login',
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: static_path('views/authentication/login.html'),
      // data: {
      //   requireLogin: false
      // },
    })
  }]);
