/*jshint esversion: 6 */
(function () {

    class DependenciaFuncional {
        constructor(implicante, implicado) {
            this.implicante = implicante;
            this.implicado = implicado;
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

        dependenciasElementales() {
            this.l1 = [];
            this.l2 = [];
            this.l3 = [];

            for (let dependencia of this.l) {
                const dependenciaArray = dependencia.split(' -> ');
                const implicante = dependenciaArray[0];
                const implicado = dependenciaArray[1];
                const variablesImplicado = implicado.split('.');

                for (let variable of variablesImplicado) {
                    const dependenciaElemental = implicante + ' -> ' + variable;
                    this.l1.push(dependenciaElemental);
                }

            }

            console.log(this.l1);
        }

        atributosExtranos() {
            this.l2 = [];
            this.l3 = [];

            for (let dependencia of this.l1) {
                const dependenciaArray = dependencia.split(' -> ');
                const implicante = dependenciaArray[0];
                const implicado = dependenciaArray[1];
                const variablesImplicante = implicante.split('.');

                for (let variable of variablesImplicante) {

                }

            }

        }

        calcularCierre(dependencias, variable) {
            for (let dependencia of dependencias) {
                const dependenciaArray = dependencia.split(' -> ');
                const implicante = dependenciaArray[0];
                const implicado = dependenciaArray[1];
                const variablesImplicante = implicante.split('.');

                let cierre = [];

                if (variablesImplicante.length === 1 && variablesImplicante[0] === variable) {
                   cierre.push(cierre);
                }

            }

        }
    }

    const t = ['a', 'b', 'c', 'd', 'e', 'f'];
    const l = ['a.b -> c', 'd -> e.f', 'c -> a', 'b.e -> c', 'b.c -> d' , 'c.f -> b.d', 'a.c.d -> b', 'c.e -> a.f'];

    const rt = new RT(t, l);

    rt.dependenciasElementales();
}());