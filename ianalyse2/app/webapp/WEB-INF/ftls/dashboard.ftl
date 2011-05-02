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
					text: 'Combination chart'
				},
				xAxis: {
					categories: ['Apples', 'Oranges', 'Pears', 'Bananas', 'Plums']
				},
				tooltip: {
					formatter: function() {
						var s = ''+
								this.x  +': '+ this.y;
						return s;
					}
				},
				labels: {
					items: [{
						html: 'Total fruit consumption',
						style: {
							left: '40px',
							top: '8px',
							color: 'black'
						}
					}]
				},
				series: [{
					type: 'column',
					name: 'Jane',
					data: [3, 2, 1, 3, 4]
				}, {
					type: 'column',
					name: 'John',
					data: [2, 3, 5, 7, 6]
				}, {
					type: 'column',
					name: 'Joe',
					data: [4, 3, 3, 9, 0]
				}, {
					type: 'spline',
					name: 'Average',
					data: [3, 2.67, 3, 6.33, 3.33]
				}]
			});


		});
</script>

<h1>Passed/Failed builds between projects<h1>
<div id="container"></div>


</body>
</html>
