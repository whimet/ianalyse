function render_commitors(json, id) {
        var chart = new Highcharts.Chart({
        chart: {
            renderTo: id
        },
        title: {
            text: ''
        },
        xAxis: {
            categories:json["names"],
            labels: { rotation: 45, align: 'left' }
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
            name: 'Failed',
            color: 'red',
            type: 'column',
            data: json["failed"]
        },{
            name: 'Passed',
            color: '#89A54E',
            type: 'column',
            data: json["passed"]
        }]
    });
}