
function plot_occupation_dist(mydata) {
    google.charts.load("current", {packages:["corechart"]});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['职业', '人数'],
          ['本科生' + mydata.typeDist.U + '人', mydata.typeDist.U],
          ['硕士生' + mydata.typeDist.M + '人', mydata.typeDist.M],
          ['博士生' + mydata.typeDist.D + '人', mydata.typeDist.D],
          ['公司职员' + mydata.typeDist.E + '人', mydata.typeDist.E],
          ['教职/研究员' + mydata.typeDist.R + '人', mydata.typeDist.R]
        ]);

        var options = {
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_occup'));
        chart.draw(data, options);
    }
}

function plot_sex_dist(mydata) {
    google.charts.load("current", {packages:["corechart"]});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['性别', '人数'],
          ['女' + mydata.sexDist['2'] + '人', mydata.sexDist['2']],
          ['男' + mydata.sexDist['1'] + '人', mydata.sexDist['1']],
          ['其他' + mydata.sexDist['0'] + '人', mydata.sexDist['0']]
        ]);

        var options = {
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_sex'));
        chart.draw(data, options);
    }
}

$.get('group_summary.json', function(data){
    plot_occupation_dist(data)
    plot_sex_dist(data)
    Object.keys(data.cityDist).forEach(function(key,index) {
        for (j=0; j< data.cityDist[key]; j++)
            console.info(key)
    });
})

