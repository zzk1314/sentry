import React from 'react';
import ReactEcharts from 'echarts-for-react';
import moment from 'moment/moment';
import theme from 'app/utils/theme';
import _ from 'lodash';

const {data} = require('./transData.js');

export default class Chart extends React.Component {
  getLineSeries = () => {
    const lineSeries = _.groupBy(data, (dataPoint) => {return dataPoint['tags[transaction]']});
    return lineSeries;
  };

  getColorList(idx) {
    return [theme.blueDark, theme.gray2, theme.purple,
              theme.orangeDark, theme.gray5, theme.purpleDark][idx % 5]
  }

 defineSeries = ([key, value], idx) => {
   console.log(idx)
   return {
    name: key,
    type: 'line',
    // areaStyle: {normal: {}},
    data: value.map(entry => entry.count), //TODO: make reusable
    color: this.getColorList(idx), //function for color picking
    }
  };

  getOption = () => {
    const labels = data.map(entry => moment(entry.time).format('MM-DD'));
    const dataset = this.getLineSeries();

    const series = Object.entries(dataset).map(this.defineSeries)
    console.log('series', series)

    return {
      title: {
        text: 'Echarts Demo',
      },
      tooltip: {
        trigger: 'axis', // or 'item' // https://ecomfe.github.io/echarts-doc/public/en/option.html#tooltip.trigger
      },
      legend: {
        data: labels,
      },
      toolbox: {
        feature: {
          saveAsImage: {},
        },
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: labels,
        },
      ],
      yAxis: [
        {
          type: 'value',
        },
      ],
      series,
      //   [
      //   {
      //     name: 'Aggregate Events over Time',
      //     type: 'line',
      //     stack: 'Aggregates',
      //     areaStyle: {normal: {}},
      //     data: dataSet,
      //     color: theme.blueDark,
      //   },
      //   {
      //     name: 'Aggregate Events over Time 2',
      //     type: 'line',
      //     stack: 'Aggregates 2',
      //     areaStyle: {normal: {}},
      //     data: dataSet2,
      //     color: theme.gray2,
      //   },
      // ],
    };
  };

  render() {
    console.log("touches render");
    return (
      <div>
        <ReactEcharts
          option={this.getOption()}
          style={{height: '350px', width: '100%'}}
          className="react_for_echarts"
        />


      </div>
    );
  }
}
