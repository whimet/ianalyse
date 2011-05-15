<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Projects</title>
	<!-- Framework CSS -->
	<link rel="stylesheet" href="/ianalyse2/css/screen.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/ianalyse2/css/plugins/buttons/screen.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/ianalyse2/css/main.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/ianalyse2/css/print.css" type="text/css" media="print">
	<!--[if lt IE 8]><link rel="stylesheet" href="/ianalyse2/css/ie.css" type="text/css" media="screen, projection"><![endif]-->

    <script type="text/javascript" src="/ianalyse2/javascripts/jquery-1.5.2.min.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/highcharts.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/exporting.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/commitors.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/per-build.js"></script>
</head>
<body>
    <div class="container" id="header">
		<span id="title">iAnalyze</span>
		<span id="subtitle">&nbsp;&nbsp;&nbsp;&nbsp;Tell more about your builds</span>
	</div>
	<br/>

	<div class="container">
		<h2>Passed and failed checkins for the commitors</h2>
        <div id="per-commitor">
        </div>
        <script>
        jQuery(document).ready(function() {
        $.ajax({
          url: "/ianalyse2/project/${project}/commitors.json",
          success: function(data, textStatus, jqXHR){
                var obj = jQuery.parseJSON(jqXHR.responseText);
                render_commitors(obj, "projects-${project}")
          }
        });
        })
        </script>
	</div>
	<div class="container">
		<h2>Date and Time of each build</h2>
        <div id="per-build">
        </div>
        <script type="text/javascript">
        jQuery(document).ready(function() {
        $.ajax({
          url: "/ianalyse2/project/${project}/perbuild.json",
          success: function(data, textStatus, jqXHR){
                var obj = jQuery.parseJSON(jqXHR.responseText);
                per_build(obj,
                "http://deadlock.netbeans.org/hudson/job/${project}/")
          }
        });
        })


        </script>

	</div>

	<br/>
	<div id="footer" class="container">
		<hr/>
		<a href="#">contributors</a> | <a href="#">project home page</a>
		<hr class="space"/>
	</div>
</body>
</html>
