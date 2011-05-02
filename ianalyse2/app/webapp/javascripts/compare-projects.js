jQuery(document).ready(function() {
    render_compare_projects(
            ['analystic-server', 'lnp'],
            [3, 1],
            [10, 12],
            [49.9, 71.5])
})

function render_compare_projects(names, failed, passed, rate) {
        var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container'
        },
        title: {
            text: 'Pass rate and build times between projects'
        },
        xAxis: {
            categories: names
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
            data: failed
        },{
            name: 'Builds',
            color: '#89A54E',
            type: 'column',
            data: passed
        }
        ,{
            name: 'Pass rate',
            color: '#4572A7',
            type: 'spline',
            yAxis: 1,
            data: rate

        }]
    });
}