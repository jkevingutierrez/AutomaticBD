﻿(function() {
    'use strict';

    angular
        .module('AutomaticBD')
        .controller('MainController', MainController);

    MainController.$inject = ['$scope', '$http', '$location', 'messages', 'SweetAlert'];

    /**
     * @namespace MainController
     */
    function MainController($scope, $http, $location, messages, SweetAlert) {
        // Classes
        var Model = function() {
            if (this instanceof Model) {
                this.atributos = [];
                this.dependencias = [];
            } else {
                return new Model();
            }
        };

        var Dependency = function() {
            if (this instanceof Dependency) {
                this.implicante = [];
                this.implicado = [];
            } else {
                return new Dependency();
            }
        };

        var baseUrl = $location.absUrl();
        var vm = this;

        vm.dependencies = [];

        vm.atributos = [];

        vm.solution = {};

        vm.initialJson = new Model();

        vm.hasFinishedLoading = true;

        vm.hasErrors = false;

        vm.loadModel = loadModel;

        vm.initPanel = initPanel;

        vm.calculateKeys = calculateKeys;

        vm.exportFile = exportFile;

        vm.exportMinimalCover = exportMinimalCover;

        vm.closePoUp = closePopUp;

        vm.showPopUp = showPopUp;

        vm.clearFile = clearFile;

        vm.clearModel = clearModel;

        vm.addDependency = addDependency;

        vm.removeDependency = removeDependency;

        vm.transformDependencies = transformDependencies;

        vm.replaceNonAlphaNumeric = replaceNonAlphaNumeric;

        vm.sortOnSelect = sortOnSelect;

        vm.initTabs = initTabs;

        vm.formatKeys = formatKeys;

        function addDependency() {
            if (!vm.initialJson.atributos || vm.initialJson.atributos.length === 0) {
                var message = 'Error agregando la dependencia: Para agregar una dependencia debe existir al menos un atributo.';
                console.error(message);
                messages.error(message);
            } else {
                var dependency = {
                    implicante: [],
                    implicado: []
                };
                vm.initialJson.dependencias.push(dependency);
            }
        }

        function removeDependency($index) {
            SweetAlert.swal({
                    title: '¿Desea continuar?',
                    text: 'Esta a punto de eliminar una dependencia. Esta operación no se puede deshacer.',
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'Continuar',
                    cancelButtonText: 'Cancelar'
                },
                function(isConfirm) {
                    if (isConfirm) {
                        var message = 'La dependencia ha sido eliminada exitosamente.';
                        messages.success(message);
                        vm.initialJson.dependencias.splice($index, 1);
                    }
                });
        }

        function loadModel($event) {
            if (vm.initialJson.atributos && vm.initialJson.atributos.length > 0 && vm.initialJson.dependencias && vm.initialJson.dependencias.length > 0) {
                SweetAlert.swal({
                        title: '¿Desea continuar?',
                        text: 'Agregar un nuevo archivo borrara el modelo actual.',
                        type: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#DD6B55',
                        confirmButtonText: 'Continuar',
                        cancelButtonText: 'Cancelar'
                    },
                    function(isConfirm) {
                        if (isConfirm) {
                            uploadFile($event);
                        }

                    });
            } else {
                uploadFile($event);
            }
        }

        function uploadFile($event) {
            console.log('uploadFile:');
            console.log($event);

            // FileList object
            var files = $event.target.files;

            // Loop through the FileList and render image files as thumbnails.
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                var reader = new FileReader();

                // Closure to capture the file information.
                reader.onload = (onLoadHandler)(file);

                reader.readAsText(file);
            }
        }

        function clearFile() {
            SweetAlert.swal({
                    title: '¿Desea continuar?',
                    text: 'Esta a punto de borrar el archivo seleccionado. Esta operación también eliminará los atributos y las dependencias existentes.',
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'Continuar',
                    cancelButtonText: 'Cancelar'
                },
                function(isConfirm) {
                    if (isConfirm) {
                        var message = 'El archivo y el modelo han sido eliminados exitosamente.';
                        messages.success(message);
                        vm.hasErrors = false;
                        vm.currentFile = undefined;
                        vm.solution = undefined;
                        vm.initialJson = new Model();
                        vm.atributos = vm.initialJson.atributos || [];
                        $('input[type=file]').val('');
                    }
                });
        }

        function clearModel() {
            SweetAlert.swal({
                    title: '¿Desea continuar?',
                    text: 'Esta a punto de borrar el modelo actual.',
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'Continuar',
                    cancelButtonText: 'Cancelar'
                },
                function(isConfirm) {
                    if (isConfirm) {
                        var message = 'El modelo ha sido eliminado exitosamente.';
                        messages.success(message);
                        vm.hasErrors = false;
                        vm.solution = undefined;
                        vm.initialJson = new Model();
                        vm.atributos = vm.initialJson.atributos || [];
                    }
                });
        }

        function onLoadHandler(theFile) {
            return function(event) {
                console.log('onLoadHandler:');
                console.log(event);
                var result = event.target.result;
                var json = new Model();
                var message = '';

                vm.solution = undefined;

                try {
                    vm.hasErrors = false;
                    var temporalJson = JSON.parse(result);

                    if (temporalJson.dependencias && temporalJson.atributos && temporalJson.dependencias.length > 0 && temporalJson.atributos.length > 0) {
                        json = JSON.parse(result);
                        message = 'El archivo <i>' + theFile.name + '</i> se ha cargado exitosamente.';
                        messages.success(message);
                    } else {
                        vm.hasErrors = true;
                        message = 'Error cargando el archivo <i>' + theFile.name + '</i>';
                        message += ': El archivo no contiene dependencias o atributos.';

                        console.error(message);
                        messages.error(message);
                    }
                } catch (error) {
                    vm.hasErrors = true;
                    message = 'Error cargando el archivo <i>' + theFile.name + '</i>';
                    if (error) {
                        message += ': ' + error;
                    }

                    console.error(error);
                    messages.error(message);
                }

                $scope.$apply(function() {
                    vm.initialJson = angular.copy(json);
                    vm.initialJson.atributos.sort();
                    vm.currentFile = {
                        name: theFile.name,
                        size: theFile.size,
                        type: theFile.type
                    };
                    vm.atributos = vm.initialJson.atributos || [];
                    vm.dependencies = vm.initialJson.dependencias || [];
                });

            };
        }

        function initPanel() {
            function toggleChevron(e) {

                var $panelHeading = $(e.target).prev('.panel-heading');

                $panelHeading
                    .find('i.indicator')
                    .toggleClass('glyphicon-menu-down glyphicon-menu-up');
            }

            $('#accordion, #accordion-initial').on('hidden.bs.collapse', toggleChevron);
            $('#accordion, #accordion-initial').on('shown.bs.collapse', toggleChevron);
            $('#accordion, #accordion-initial').click(function(e) {
                e.preventDefault();
            });
        }

        function showPopUp($event) {
            var el = $event.currentTarget;

            $('#helpPopup').css({
                'left': el.offsetLeft - el.scrollLeft + 10,
                'top': el.offsetTop - el.scrollTop + 10
            });
            $('#helpPopup').toggle('fast');

            if ($('#helpPopup').offset().left + $('#helpPopup').width() > $(window).width()) {
                $('#helpPopup').css({
                    'left': el.offsetLeft - el.scrollLeft - $('#helpPopup').width() + 10,
                    'top': el.offsetTop - el.scrollTop + 10
                });
            }
        }

        function closePopUp() {
            $('#helpPopup').hide('fast');
        }

        function getJsonFromUrl(url) {
            $http({
                method: 'GET',
                url: url,
                contentType: 'application/json; charset=utf-8'
            }).then(function(response) {
                console.log('getJsonFromUrl:');
                console.log(response);
                if (response.data) {
                    var message = 'El archivo de ejemplo se ha cargado exitosamente.';
                    messages.success(message);
                    var json = response.data;
                    vm.jsonExample = json;
                }
            }).catch(function(error) {
                var message = 'Error leyendo el archivo JSON desde <i>' + url + '</i>';
                if (typeof error === 'string') {
                    message += ': ' + error;
                } else if (error & error.statusText) {
                    message += ': ' + error.statusText();
                }
                console.error(error);
                messages.error(message);
            });
        }

        function exportFile(json, fileName) {
            $http({
                method: 'POST',
                url: baseUrl + 'file',
                data: json,
                contentType: 'application/json; charset=utf-8',
                dataType: 'json'
            }).then(function(response) {
                console.log('exportFile');
                console.log(response);
                if (response.data) {
                    var message = 'El archivo <i>' + fileName + '</i> se ha generado exitosamente.';
                    messages.success(message);
                    var json = response.data;
                    saveFile(JSON.stringify(json, null, 4), fileName);
                }
            }).catch(function(error) {
                var message = 'Error exportando el archivo <i>' + fileName + '</i>';
                if (typeof error === 'string') {
                    message += ': ' + error;
                } else if (error & error.statusText) {
                    message += ': ' + error.statusText();
                }
                console.error(error);
                messages.error(message);
            });
        }

        function exportMinimalCover(json, fileName) {
            var output = {
                atributos: vm.initialJson.atributos,
                dependencias: json.l3
            };
            exportFile(output, fileName);
        }

        function saveFile(data, fileName) {
            var a = document.createElement('a');
            a.style = 'display: none';
            document.body.appendChild(a);
            var blob = new Blob([data], { type: 'octet/stream' });
            var url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = fileName;
            a.click();
            window.URL.revokeObjectURL(url);
        }

        function calculateKeys(json) {
            if (json && json.atributos && json.atributos.length > 0 && json.dependencias && json.dependencias.length > 0) {
                $http({
                    method: 'POST',
                    url: baseUrl + 'api',
                    data: json,
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json'
                }).then(function(response) {
                    console.log('calculateKeys:');
                    console.log(response);
                    if (response.data) {
                        var message = 'Se han calculado las llaves candidatas exitosamente y, se ha generado el archivo <i>Salida.txt</i>, el cual contiene el registro de las operaciones.';
                        messages.success(message);
                        vm.solution = {};
                        vm.solution = response.data;
                        saveFile(vm.solution.file, 'Salida.txt');

                        console.log('L1: ', transformDependencies(vm.solution.l1));
                        console.log('L2: ', transformDependencies(vm.solution.l2));
                        console.log('L3: ', transformDependencies(vm.solution.l3));
                        console.log('Llaves: ', vm.solution.keys);
                    }
                }).catch(function(error) {
                    var message = 'Error calculando el recubrimiento mínimo';
                    if (typeof error === 'string') {
                        message += ': ' + error;
                    } else if (error & error.statusText) {
                        message += ': ' + error.statusText();
                    }
                    console.error(error);
                    messages.error(message);
                });
            } else {
                var message = 'Error calculando el recubrimiento mínimo: La estructura del modelo JSON es incorrecta.';
                console.error(message);
                messages.error(message);
            }

        }

        function formatKeys(keys) {
            var text = '[ ';

            for (var keyIndex = 0; keyIndex < keys.length; keyIndex++) {
                var key = keys[keyIndex];

                if (typeof key === 'string') {
                    text += keys.join(', ');
                    break;
                } else if (key instanceof Array && key.length > 0) {
                    for (var varIndex = 0; varIndex < key.length; varIndex++) {
                        text += '(';
                        text += key.join(', ');
                        if (keyIndex === keys.length) {
                            text += ')';
                        } else {
                            text += '), ';
                        }
                    }
                }
            }

            text += ' ]';
            return text;
        }

        function transformDependencies(dependencies) {
            console.log('Transformar dependencias');
            console.log(dependencies);
            var textArray = [];

            if (dependencies) {
                dependencies.forEach(function(dependency) {
                    dependency.implicante = Array.from(dependency.implicante);
                    dependency.implicado = Array.from(dependency.implicado);
                    textArray.push(dependency.implicante.join('.') + ' -> ' + dependency.implicado.join('.'));
                });
            }

            return '{ ' + textArray.join(', ') + ' }';
        }

        function replaceNonAlphaNumeric($item) {
            var lastIndex = vm.initialJson.atributos.length - 1;

            if ($item) {
                var itemWithNonAlphanumeric = $item.toLowerCase().replace(/\W+/g, '');
                vm.initialJson.atributos[lastIndex] = itemWithNonAlphanumeric;
            } else {
                vm.initialJson.atributos.splice(lastIndex, 1);
            }

            vm.initialJson.atributos.sort();
        }

        function sortOnSelect(list) {
            list.sort();
        }

        function initTabs() {
            $('#tabs a').click(function(e) {
                console.log('click');
                e.preventDefault();
                $(this).tab('show');
            });
        }

        function main() {
            getJsonFromUrl(window.exampleJson);
        }


        main();
    }

})();
