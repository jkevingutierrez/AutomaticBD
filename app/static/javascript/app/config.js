(function() {
    'use strict';

    angular
        .module('AutomaticBD')
        .config(config);

    config.$inject = ['$interpolateProvider', '$locationProvider', '$provide', '$httpProvider', '$routeProvider'];

    /**
     * @name config
     * @desc Define valid application routes and some configuration stuffs
     */
    function config($interpolateProvider, $locationProvider, $provide, $httpProvider, $routeProvider) {
        httpInterceptor.$inject = ['$q', '$rootScope'];

        function httpInterceptor($q, $rootScope) {
            return {
                'request': function(config) {
                    //Aca se muestra el diálogo de cargando. Se ignoran los casos en que lee un template o una imagen svg
                    if (config.url.indexOf('.svg') === -1 && config.url.indexOf('.html') === -1 && config.url.indexOf('/getStatusDescription/') === -1) {
                        $rootScope.isLoading = true;
                    }
                    config.headers['X-Requested-With'] = 'XMLHttpRequest';

                    $rootScope.$broadcast('httpRequest', config);
                    return config || $q.when(config);
                },
                'response': function(response) {
                    //Aca se oculta el diálogo
                    if (response.config.url.indexOf('.svg') === -1 && response.config.url.indexOf('.html') === -1) {
                        $rootScope.isLoading = false;
                    }

                    $rootScope.$broadcast('httpResponse', response);
                    return response || $q.when(response);
                },
                'requestError': function(rejection) {
                    $rootScope.isLoading = false;

                    $rootScope.$broadcast('httpRequestError', rejection);
                    return $q.reject(rejection);
                },
                'responseError': function(rejection) {
                    $rootScope.isLoading = false;

                    if (rejection.status == 901) {
                        window.location.reload(true);
                        return;
                    }

                    $rootScope.$broadcast('httpResponseError', rejection);
                    return $q.reject(rejection);
                }
            };
        }

        $provide.factory('httpInterceptor', httpInterceptor);

        $httpProvider.interceptors.push('httpInterceptor');

        $routeProvider.when('/', {
            templateUrl: 'static/javascript/app/templates/main.html',
            controller: 'MainController',
            controllerAs: 'vm'
        }).otherwise({
            redirectTo: '/'
        });

        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');

        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        // $locationProvider.html5Mode(false);
        // $locationProvider.hashPrefix("!");
    }

})();
