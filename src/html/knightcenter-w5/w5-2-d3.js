

var width = 900,
    height = 400;

// lookup table: country code -> country 
var countryByCode = {}

// lookup table: country code -> climate data 
var dataByCode = {}

// selected country
var currentCode;





// D3 Global variables ---------------------------------

var path = d3.geo.path();

var body = d3.select("body");

var svg = d3.select("#map").append("svg")
    .attr("width", width)
    .attr("height", height);


/*
  =====================================
    Select Country Component
  

  =====================================
*/
select = function(){
    
    var x=800, y=20;

    var g =  svg.append("g")
        .attr("class", "select")
        .attr('transform', 'translate(' + x + ',' + y + ')');


    //
    function draw(countries, temparatures){
        
        d3.select("#countries")
            .on("change",change)
            .selectAll("option")
            .data(countries)
            .enter().append("option")
            .attr("value", function(d) { return d.code;})
            .text(function(d) { return d.name;});
         
        g.append("svg:text")
            .attr("x", 0)
            .attr("y", 0)
            .attr("class","title")
            .text('');

        g.append("svg:text")
            .attr("x", 0)
            .attr("y", 30)
            .attr("class","subtitle")
            .attr("id", "region")
            .text('');

        g.append("svg:text")
            .attr("x", 0)
            .attr("y", 50)
            .attr("class","subtitle")
            .attr("id", "incg")
            .text('');

    }

    //
    function change(){
        
        currentCode = this.value
        refresh();

    }

    // 
    function update(){

        g.select(".title").text(countryByCode[currentCode].name);
        g.select("#region").text(countryByCode[currentCode].region);
        g.select("#incg").text(countryByCode[currentCode].incomegroup);
     
    }

    // public
    return {

        draw: draw,
        update: update,
        change: change

    }


}();

/*
  =====================================
    Graph Component
  

  =====================================
*/
graph = function(){
    
    var posx=30, posy=0;

    var g =  svg.append("g")
        .attr("class", "select")
        .attr('transform', 'translate(' + posx + ',' + posy + ')');

    var data = {};

    var x = d3.scale.ordinal()
            .rangeBands([0, 300], 0.1);

    var y = d3.scale.linear()
        .range([300, 30]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("right");

    x.domain(['1960-2000','2045-2060']);

    //
    function draw(countries, temparatures){

        g.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0,300)")
              .call(xAxis);

        g.append("g")
              .attr("class", "y axis")
              .call(yAxis)
              .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", -20)
              .attr("x", -60)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("Temperature (°C)");

        ['1960-2000','2045-2060'].forEach(function(v){
            g.append("rect")
            .attr('class', 'baryear')
            .attr("x", x(v) + 40)
            .attr("y", 30)
            .attr("width", 50)
            .attr("height", 270);

        });

    }

    function temperatures(){

        var temp = dataByCode[currentCode];
        //console.log(temp);
        var  o1 = {};
        var o2 = {};
        o1.period = '1960-2000';
        o1.tmin = parseFloat(temp.tmin);
        o1.tmax = parseFloat(temp.tmax);
        o2.period = '2045-2060';
        o2.tmin = o1.tmin + parseFloat(temp.pmin);
        o2.tmax = o1.tmax + parseFloat(temp.pmax);
        return [o1,o2];

    }


    // 
    function update(){

        data = temperatures();
        min = d3.min(data, function(d) { return d.tmin; }) - 2;
        max = d3.max(data, function(d) { return d.tmax; }) + 2;
        y.domain([min, max]);

        g.selectAll(".tmin").remove();
        g.selectAll(".tmax").remove();
        
        g.select(".y.axis").call(yAxis);
        g.select(".x.axis").call(xAxis);

        g.selectAll("circle.tmin")
            .data(data)
            .enter().append("circle")
            .attr('class', 'tmin')
            .attr("cx", function(d) { return x(d.period) + 65})
            .attr("cy", function(d) { return y(d.tmin)})
            .attr("r", 6);
        g.selectAll("circle.tmax")
            .data(data)
            .enter().append("circle")
            .attr('class', 'tmax')
            .attr("cx", function(d) { return x(d.period) + 65})
            .attr("cy", function(d) { return y(d.tmax)})
            .attr("r", 6);

        data.forEach(function(d,i){

            g.append("svg:text")
                .attr('class', 'tmin')
                .attr("x", x(d.period) + 60)
                .attr("y", y(d.tmin) - 6)
                .text(d3.format('+,.1f')(d.tmin)); 
            g.append("svg:text")
                .attr('class', 'tmax')
                .attr("x", x(d.period) + 60)
                .attr("y", y(d.tmax) - 6)
                .text(d3.format('+,.1f')(d.tmax)); 

        });
        



     
    }

    // public
    return {

        draw: draw,
        update: update

    }


}();





//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
	     

/*
  Load resources.
*/
queue()
	    .defer(d3.csv, "data/countries.csv")
        .defer(d3.csv, "data/temperatures.csv")
	    .await(ready);

/*
  All graphic components.
*/
var components = [select, graph];


/*
  Ready:
*/
function ready(error, countries, temperatures) {

    //
    temperatures.forEach(function(d){
        dataByCode[d.code] = d;
    });
    var tmp = []
    countries.forEach(function(d){
        if (dataByCode[d.code] != undefined){
            countryByCode[d.code] = d;
            tmp.push(d);
        }
    });
    countries = tmp;

    // draw D3 components
    components.forEach(function(c){
          c.draw(countries, temperatures);
    });

    currentCode = 'USA';
    d3.select("#countries")[0][0].value = currentCode;
    refresh();
     
}

/*
  Refresh:
*/
function refresh(){

      // update D3 components
      components.forEach(function(c){
          c.update();
      });
    
}
