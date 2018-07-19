import React from 'react';
import ReactEcharts from 'echarts-for-react';
import moment from 'moment/moment';
import theme from 'app/utils/theme';

const {data} = require('./tempData.js');

export default class chart extends React.Component {
  getOption = () => ({
    title: {
      show: false,
      // text: 'bar chart'
    },
    tooltip: {},
    legend: {
      data: ['legend-data'],
    },
    xAxis: {
      data: ['a', 'b', 'c', 'd', 'e', 'f'],
    },
    grid: {
      top: 20,
    },
    yAxis: {},
    series: [
      {
        name: 'series name',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20],
        itemStyle: {
          normal: {
            color: function(params) {
              const colorList = [
                theme.blueDark,
                theme.gray2,
                theme.purple,
                theme.orangeDark,
                theme.gray5,
                theme.purpleDark,
              ];
              return colorList[params.dataIndex];
            },
          },
        },
      },
    ],
  });

  render() {
    return (
      <div>
        <ReactEcharts
          option={this.getOption()}
          style={{height: '350px', width: '100%'}}
          className="react_for_echarts"
          opts={{renderer: 'svg'}}
        />
      </div>
    );
  }
}
