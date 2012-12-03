
Tangle.classes.FilterTimePlot = {

    initialize: function (el, options, tangle) {
        this.tangle = tangle;
    },

    update: function (el, kf, kq) {
        var canvasWidth = el.get("width");
        var canvasHeight = el.get("height");
        var ctx = el.getContext("2d");

        var fs = this.tangle.getValue("fs");
        var unstable = this.tangle.getValue("unstable");
        var widthBeforeStep = this.getWidthBeforeStep();

        var N = 256;
        var values = chamberlinStepResponse(kf,kq,N);

        ctx.fillStyle = "#fff";
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);

        ctx.strokeStyle = unstable ? "#f00" : "#00f";
        ctx.lineWidth = 2;
        ctx.beginPath();

        ctx.moveTo(0, canvasHeight-1);
        ctx.lineTo(widthBeforeStep, canvasHeight-1);

        for (var x = widthBeforeStep; x < canvasWidth; x++) {
            var i = x - widthBeforeStep;
            var fracI = i - Math.floor(i);
            var lowV = values[Math.floor(i)];
            var highV = values[Math.ceil(i)];
            var value = lowV + fracI * (highV - lowV);
            var y = value * canvasHeight/2;
            ctx.lineTo(x, canvasHeight - y);
        }

        ctx.stroke();
    },

    getWidthBeforeStep: function () { return 16; }
};

