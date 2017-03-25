(function() {
    'use strict';

    angular.module('AutomaticBD', ['ngRoute', 'ui.select', 'ngSanitize']);

    angular.element(document).ready(function() {
        angular.bootstrap(document.body, ['AutomaticBD']);
    });

})();
