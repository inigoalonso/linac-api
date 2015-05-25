function loadPlot( plotId ) {
	$('#plotIframe').setAttribute( 'src', "https://plot.ly/~ess/"+plotId+".embed?width=750&height=517.5");
	document.getElementById('plotIframe').contentWindow.location.reload();
}