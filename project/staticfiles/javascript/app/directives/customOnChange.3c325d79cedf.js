(function() {
    'use strict';

    angular
        .module('AutomaticBD')
        .directive('customOnChange', CustomOnChange);

    /**
     * @namespace CustomOnChange
     */
    function CustomOnChange() {
        return {
            restrict: 'A',
            link: function($scope, $element, $attrs) {
                var onChangeHandler = $scope.$eval($attrs.customOnChange);
                $element.bind('change', onChangeHandler);
            }
        };
    }

})();
