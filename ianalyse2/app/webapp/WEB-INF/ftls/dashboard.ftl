<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <script type="text/javascript" src="/ianalyse2/javascripts/jquery-1.5.2.min.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/highcharts.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/exporting.js"></script>
</head>
<body>
<script type="text/javascript">
	Highcharts.theme = { colors: ['#4572A7'] };// prevent errors in default theme
	var highchartsOptions = Highcharts.getOptions();
</script>

<script type="text/javascript">
		var chart;
		jQuery(document).ready(function() {
			chart = new Highcharts.Chart({
				chart: {
					renderTo: 'container'
				},
				title: {
					text: 'Pass rate and build times between projects'
				},
				xAxis: {
					categories: ['analystic-server', 'lnp']
				},
				yAxis: [{ // Primary yAxis
					labels: {
						formatter: function() {
							return this.value +'times';
						},
						style: {
							color: '#89A54E'
						}
					},
					title: {
						text: 'Builds',
						style: {
							color: '#89A54E'
						}
					}
				}, { // Secondary yAxis
					title: {
						text: 'Pass rate',
						style: {
							color: '#4572A7'
						}
					},
					labels: {
						formatter: function() {
							return this.value +' %';
						},
						style: {
							color: '#4572A7'
						}
					},
					opposite: true
				}],
				tooltip: {
					formatter: function() {
						var s = ''+
								this.x  +': '+ this.y;
						return s;
					}
				},
				labels: {
					items: [{
						html: '',
						style: {
							left: '40px',
							top: '8px',
							color: 'black'
						}
					}]
				},
				plotOptions: {
					column: {
						stacking: 'normal'
					}
				},
				series: [
				{
					name: 'Builds',
					color: 'red',
					type: 'column',
					data: [3, 1]
				},{
					name: 'Builds',
					color: '#89A54E',
					type: 'column',
					data: [10, 12]
				}
				,{
					name: 'Pass rate',
					color: '#4572A7',
					type: 'spline',
					yAxis: 1,
					data: [49.9, 71.5]

				}]
			});


		});
</script>

<h1>Passed/Failed builds between projects hah<h1>
<div id="container"></div>


</body>
</html>
