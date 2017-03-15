/*jshint esversion: 6 */

(function () {

    class Cierre {
        constructor(variables, dependencias) {
            this.variables = variables;
            this.dependencias = dependencias;
            this.elementos = [];
        }

        calcularCierre(dependencias, variable) {

        }

    }

    class Conversor {

        transformarART(json) {
            const variables = json.t || [];
            const dependencias = json.l || [];
            let dependenciasFuncionales = [];
            for (let dependencia of dependencias) {
                if (typeof dependencia === 'string') {
                    const dependenciaArray = dependencia.split(' -> ');

                    if (dependenciaArray.length === 2) {
                        const implicante = dependenciaArray[0];
                        const implicado = dependenciaArray[1];
                        const variablesImplicante = implicante.split('.');
                        const variablesImplicado = implicado.split('.');

                        if (variablesImplicado.length > 0 && variablesImplicante.length > 0 ) {
                            const dependenciaFuncional = new DependenciaFuncional(variablesImplicante, variablesImplicado);
                            dependenciasFuncionales.push(dependenciaFuncional);
                        }
                    }
                }
            }

            const rt = new RT(variables, dependenciasFuncionales);
            return rt;
        }

        transformarART2(json) {
            const variables = json.t || [];
            const dependencias = json.l || [];
            let dependenciasFuncionales = [];
            for (let dependencia of dependencias) {
                if (dependencia.implicante && dependencia.implicado && dependencia.implicante instanceof Array && dependencia.implicado instanceof Array && dependencia.implicante.length > 0 && dependencia.implicado.length > 0) {
                    const dependenciaFuncional = new DependenciaFuncional(dependencia.implicante, dependencia.implicado);
                    dependenciasFuncionales.push(dependenciaFuncional);
                }
            }

            const rt = new RT(variables, dependenciasFuncionales);
            return rt;
        }

        transformarATexto(dependencias) {
            let textoDependencias = [];
            for (let dependencia of dependencias) {
                textoDependencias.push(dependencia.variablesImplicante.join('.') + ' -> ' + dependencia.variablesImplicado.join('.'));
            }

            return textoDependencias;
        }
    }

    class DependenciaFuncional {
        constructor(variablesImplicante = [], variablesImplicado = []) {
            this.variablesImplicante = variablesImplicante;
            this.variablesImplicado = variablesImplicado;

            if (typeof variablesImplicado === 'string') {
                this.variablesImplicado = [variablesImplicado];
            }
        }
    }

    class RT {
        constructor(t, l) {
            this.t = t;
            this.l = l;
            this.l1 = [];
            this.l2 = [];
            this.l3 = [];
        }

        buscarDependencia(dependencia, dependencias) {
            const dependenciaEncontrada = dependencias.find(
                dependenciaActual =>
                    dependenciaActual.variablesImplicado.equals(dependencia.variablesImplicado) &&
                    dependenciaActual.variablesImplicante.equals(dependencia.variablesImplicante)
            );

            return dependenciaEncontrada ? true : false;
        }

        dependenciasElementales() {
            this.l1 = [];
            this.l2 = [];
            this.l3 = [];

            for (let dependencia of this.l) {
                const existeDependencia = this.buscarDependencia(dependencia, this.l1);
                if (dependencia.variablesImplicado.length === 1 && !existeDependencia) {
                    this.l1.push(dependencia);
                } else {
                    for (let variable of dependencia.variablesImplicado) {
                        const nuevaDependencia = new DependenciaFuncional(dependencia.variablesImplicante, variable);
                        const existeNuevaDependencia = this.buscarDependencia(nuevaDependencia, this.l1);
                        if (!existeNuevaDependencia) {
                            this.l1.push(nuevaDependencia);
                        }
                    }
                }
            }

            return this.l1;
        }

        atributosExtranos() {
            this.l2 = [];
            this.l3 = [];

            let cierre = {};

            for (let dependencia of this.l1) {
                const existeDependencia = this.buscarDependencia(dependencia, this.l2);

                if (dependencia.variablesImplicante.length === 1 && !existeDependencia) {
                    this.l2.push(dependencia);
                } else {
                    let longitud = dependencia.variablesImplicante.length;
                    let variablesTemporales = dependencia.variablesImplicante.slice();

                    for (let variable of dependencia.variablesImplicante) {
                        if (!cierre[variable]) {
                            cierre[variable] = this.calcularCierre(variable, this.l1);
                            console.log('Cierre de', variable, ':');
                            console.log(cierre[variable]);
                        }
                    }

                    while(longitud >= 0) {
                        longitud--;
                    }
                }

            }

            return this.l2;
        }

        calcularCierre(variables, dependencias) {
            let cierre = [];
            let longitud = 0;

            if (variables instanceof Array && variables.length > 0) {
                for (let variable of variables) {
                    cierre.push(variable);
                }
            } else if (typeof variables === 'string') {
                cierre.push(variables);
            }

            while(longitud < cierre.length) {
                longitud = cierre.length;
                const cierreInicial = cierre.slice();

                for (let dependencia of dependencias) {
                    const contieneVariables = dependencia.variablesImplicante.every(elem => cierre.indexOf(elem) > -1);
                    const variableImplicado = dependencia.variablesImplicado[0];

                    if (dependencia.variablesImplicante.length <= cierreInicial.length && contieneVariables && cierre.indexOf(variableImplicado) === -1) {
                        cierre.push(dependencia.variablesImplicado[0]);
                    }
                }
            }

            return cierre;
        }
    }


    function main() {
        const json = {
            t: ['a', 'b', 'c', 'd', 'e', 'f'],
            l: ['a.b -> c', 'd -> e.f', 'c -> a', 'b.e -> c', 'b.c -> d' , 'c.f -> b.d', 'a.c.d -> b', 'c.e -> a.f']
        };

        const json2 = {
            t: ['a', 'b', 'c', 'd', 'e', 'f'],
            l: [{
                implicante: ['a', 'b'],
                implicado: ['c']
            }, {
                implicante: ['d'],
                implicado: ['e', 'f']
            }, {
                implicante: ['c'],
                implicado: ['a']
            }, {
                implicante: ['b', 'e'],
                implicado: ['c']
            }, {
                implicante: ['b', 'c'],
                implicado: ['d']
            }, {
                implicante: ['c', 'f'],
                implicado: ['b', 'd']
            }, {
                implicante: ['a', 'c', 'd'],
                implicado: ['b']
            }, {
                implicante: ['c', 'e'],
                implicado: ['a', 'f']
            }]
        };

        console.log('JSON Inicial:');
        console.log(json);

        const helper = new Conversor();
        const rt = helper.transformarART(json);

        const rt2 = helper.transformarART2(json2);

        const l1 = rt.dependenciasElementales();
        const textoL1 = helper.transformarATexto(l1);
        console.log('L1:');
        console.log(textoL1);

        const l2 = rt.atributosExtranos();
        // const textoL2 = helper.transformarATexto(l2);
        // console.log(textoL2);
    }

    main();

}());