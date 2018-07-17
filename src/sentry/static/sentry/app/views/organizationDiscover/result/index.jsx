import React from 'react';
import PropTypes from 'prop-types';
import styled from 'react-emotion';
import {Box} from 'grid-emotion';

import AutoSelectText from 'app/components/autoSelectText';
import Chart from 'app/views/organizationDiscover/chart.jsx';
import BarChart from 'app/views/organizationDiscover/barchart.jsx';
import OurChart from 'app/components/charts/baseChart'

import _ from 'lodash';

import {getDisplayValue} from './utils';
/**
 * Renders results in a table as well as a query summary (timing, rows returned)
 * from any Snuba result
 */
export default class Result extends React.Component {
  static propTypes = {
    result: PropTypes.object.isRequired,
  };

  renderTable() {
    const {meta, data} = this.props.result;
    console.log('Table Data: ', data);
    // const x = _.groupBy(data, 'platform');
    // console.log('~~~~~ grouped by', x);
    const {renderChart} = this.props;
    return (
      <StyledTable className="table table-bordered table-hover">
        <thead>
          <tr>{meta.map(({name}, idx) => <th key={idx}>{name}</th>)}</tr>
        </thead>
        <tbody>
          {data.map((row, rowIdx) => {
            return (
              <tr key={rowIdx}>
                {meta.map((val, colIdx) => (
                  <td key={colIdx}>
                    <AutoSelectText>
                      {getDisplayValue(row[meta[colIdx].name])}
                    </AutoSelectText>
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </StyledTable>
    );
  }

  renderChart() {
    const {data} = this.props.result;
    const labels = data.map(entry => moment(entry.timestamp).format('MM-DD'));

    // this.parseData();
    return <Chart />;
  }

  parseData() {
    const {data} = this.props.result;
    const blacklisted = ['timestamp'];
    const whitelisted = ['platform', 'environment'];
    let chosen;
    let lines = [];

    let found = data[0].keys().some(r => whitelisted.includes(r));

    for (let key in data[0]) {
      if (data[0].hasOwnProperty(key)) {
        if (contains.call(whitelisted, key)) {
          // decide which field will represent lines in chart
          chosen = key;
        }
      }
    }

    if (found && chosen) {
      for (let i = 0; i < data.length; i++) {
        if (!$.inArray(data[i][chosen], lines)) {
          // get all values for field chosen to represent lines in chart
          lines.push(data[i][chosen]);
        }
      }
      for (let obj in data) {
        if (obj.hasOwnProperty(chosen)) {
          for (let item in lines) {
          }
        }
      }
    }
  }

  render() {
    const {error, timing, data} = this.props.result;
    const {renderChart} = this.props;
    console.log('Rendering Chart? - ', renderChart);

    if (error) {
      return <div>{error}</div>;
    }

    return (
      <div style={{overflowX: 'scroll'}}>
        <Summary mb={1}>
          snuba query time: {timing.duration_ms}ms, {data.length} rows
        </Summary>
        {this.renderTable()}
        {this.renderChart()}
        <BarChart/>
      </div>
    );
  }
}

const Summary = styled(Box)`
  font-size: 12px;
`;

const StyledTable = styled.table`
  font-size: 14px;
  tbody > tr > td,
  thead > tr > th {
    padding: 8px;
    max-width: 100px;
    overflow: scroll;
  }
`;
