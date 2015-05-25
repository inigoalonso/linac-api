function loadPlot(plotId) {
	var str = "<a href=\"https://plot.ly/~ess/plotId/\" target=\"_blank\" style=\"display: block; text-align: center;\"><img src=\"https://plot.ly/~ess/plotId.png\" style=\"width: 100%;\"  width=\"757\" onerror=\"this.onerror=null;this.src=\'https://plot.ly/404.png\';\" /></a><script data-plotly=\"ess:plotId\" src=\"https://plot.ly/embed.js\" async></script>";
	var res = str.replace(/plotId/g, plotId);
    document.getElementById("plotlyPlots").innerHTML = res;
}