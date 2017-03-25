(function() {
    'use strict';

    angular.module('AutomaticBD', ['ngRoute', 'ngSanitize', 'ngAlertify', 'ui.select', 'oitozero.ngSweetAlert']);

    angular.element(document).ready(function() {
        angular.bootstrap(document.body, ['AutomaticBD']);
    });

})();
