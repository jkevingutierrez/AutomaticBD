(function() {
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
                this.t = [];
                this.l = [];
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

        vm.variables = [];

        vm.solution = {};

        vm.initialJson = new Model();

        vm.hasFinishedLoading = true;

        vm.hasErrors = false;

        vm.uploadFile = uploadFile;

        vm.initPanel = initPanel;

        vm.calculateMinimalCover = calculateMinimalCover;

        vm.exportFile = exportFile;

        vm.closePoUp = closePopUp;

        vm.showPopUp = showPopUp;

        vm.clearFile = clearFile;

        vm.addDependency = addDependency;

        vm.removeDependency = removeDependency;

        function addDependency() {
            if (!vm.initialJson.t || vm.initialJson.t.length === 0) {
                var message = 'No existe ninguna variable';
                console.error(message);
                messages.error(message);
            } else {
                var dependency = {
                    implicante: [],
                    implicado: []
                };
                vm.initialJson.l.push(dependency);
            }
        }

        function removeDependency($index) {
            SweetAlert.swal({
                    title: '¿Desea continuar?',
                    text: 'Esta a punto de eliminar una dependencia. Esta operación no se puede deshacer',
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'Continuar',
                    cancelButtonText: 'Cancelar'
                },
                function(isConfirm) {
                    if (isConfirm) {
                        var message = 'La dependencia ha sido eliminada exitosamente';
                        messages.success(message);
                        vm.initialJson.l.splice($index, 1);
                    }
                });
        }

        function uploadFile($event) {
            console.log('Upload File');
            console.log($event);

            // FileList object
            var files = $event.target.files;

            // Loop through the FileList and render image files as thumbnails.
            for (var i = 0, file; file = files[i]; i++) {
                var reader = new FileReader();

                // Closure to capture the file information.
                reader.onload = (function(theFile) {
                    return function(event) {
                        console.log('On Load File');
                        console.log(event);
                        var result = event.target.result;
                        var json = new Model();

                        try {
                            vm.hasErrors = false;
                            json = JSON.parse(result);
                        } catch (error) {
                            var message = 'Error al cargar el archivo <i>' + theFile.name + '</i>: ' + error;
                            vm.hasErrors = true;
                            console.error(error);
                            messages.error(message);
                        }

                        $scope.$apply(function() {
                            vm.initialJson = angular.copy(json);
                            vm.currentFile = {
                                name: theFile.name,
                                size: theFile.size,
                                type: theFile.type
                            };
                            vm.variables = vm.initialJson.t || vm.initialJson.variables || [];
                            vm.dependencies = vm.initialJson.l || vm.initialJson.dependencias || [];
                        });

                    };
                })(file);

                reader.readAsText(file);
            }
        }

        function clearFile() {
            SweetAlert.swal({
                    title: '¿Desea continuar?',
                    text: 'Esta a punto de borrar el archivo seleccionado. Esta operación también borrara las variables y las dependencias existentes',
                    type: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'Continuar',
                    cancelButtonText: 'Cancelar'
                },
                function(isConfirm) {
                    if (isConfirm) {
                        var message = 'El archivo y el modelo han sido eliminados';
                        messages.success(message);
                        vm.hasErrors = false;
                        vm.currentFile = undefined;
                        vm.initialJson = new Model();
                        $('input[type=file]').val('');
                    }
                });
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
                'left': el.offsetLeft - el.scrollLeft + 6,
                'top': el.offsetTop - el.scrollTop + 6
            });
            $('#helpPopup').toggle('fast');

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
                console.log('Get Json From Url');
                console.log(response);
                if (response.data) {
                    var json = response.data;
                    vm.jsonExample = json;
                }
            }).catch(function(error) {
                console.error(error);
                messages.error(error);
            });
        }

        function exportFile(json) {
            $http({
                method: 'POST',
                url: baseUrl + 'file',
                data: json,
                contentType: 'application/json; charset=utf-8'
            }).then(function(response) {
                console.log('Export File');
                console.log(response);
                if (response.data) {
                    var json = response.data;
                    saveFile(JSON.stringify(json, null, 4), 'salida.json');
                }
            }).catch(function(error) {
                console.error(error);
                messages.error(error);
            });
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

        function calculateMinimalCover(json) {
            if (json && json.l && json.t && json.l.length > 0 && json.t.length > 0) {
                $http({
                    method: 'POST',
                    url: baseUrl + 'api',
                    data: json,
                    contentType: 'application/json; charset=utf-8'
                }).then(function(response) {
                    console.log('Calculate Minimal Cover');
                    console.log(response);
                    if (response.data) {
                        vm.solution = {};
                        vm.solution = response.data;
                        saveFile(vm.solution.file, 'Recubrimiento.txt');

                        console.log('L1: ', transform(vm.solution.l1));
                        console.log('L2: ', transform(vm.solution.l2));
                        console.log('L3: ', transform(vm.solution.l3));
                    }
                }).catch(function(error) {
                    console.error(error);
                    messages.error(error);
                });
            } else {
                var message = 'La estructura del json es incorrecta';
                console.error(message);
                messages.error(message);
            }

        }

        function transform(dependencies) {
            var textArray = [];

            if (dependencies) {
                dependencies.forEach(function(dependency) {
                    textArray.push(dependency.variablesImplicante.join('.') + ' -> ' + dependency.variablesImplicado.join('.'));
                });
            }

            return textArray;
        }

        function main() {
            var resource = Math.floor((Math.random() * 6) + 1);
            getJsonFromUrl(baseUrl + 'static/resource/' + resource + '.json');
        }


        main();
    }

})();
