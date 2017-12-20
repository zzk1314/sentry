import PropTypes from 'prop-types';
import React from 'react';
import styled from 'react-emotion';
import _ from 'lodash';

import ApiMixin from '../mixins/apiMixin';
import AsyncView from './asyncView';
import BarChart from '../components/barChart';
import LoadingError from '../components/loadingError';
import LoadingIndicator from '../components/loadingIndicator';

const Cell = styled.div`
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;

  strong {
    font-size: 24px;
    color: #000;
    display: block;
    font-weight: normal;

    small {
      margin-left: 5px;
      color: #999;
      font-size: 16px;
    }
  }

  .standard-barchart {
    margin: 0 -20px -20px;
    border: 0;
  }

  h6 {
    text-transform: uppercase;
    font-size: 14px;
    color: #999;
    display: block;
    margin-bottom: 10px;
  }
`;

const Chart = React.createClass({
  propTypes: {
    since: PropTypes.number.isRequired,
    resolution: PropTypes.string.isRequired,
    endpoint: PropTypes.string.isRequired,
    label: PropTypes.string,
    height: PropTypes.number,
  },

  mixins: [ApiMixin],

  getDefaultProps() {
    return {
      height: 150,
    };
  },

  getInitialState() {
    return {
      error: false,
      loading: true,
      data: null,
    };
  },

  componentWillMount() {
    this.fetchData();
  },

  componentWillReceiveProps(nextProps) {
    if (!_.isEqual(nextProps, this.props)) {
      this.setState(
        {
          loading: true,
        },
        this.fetchData
      );
    }
  },

  shouldComponentUpdate(nextProps, nextState) {
    return this.state.loading !== nextState.loading;
  },

  fetchData() {
    this.api.request(this.props.endpoint, {
      method: 'GET',
      data: {
        since: this.props.since,
        resolution: this.props.resolution,
      },
      success: data => {
        this.setState({
          data,
          loading: false,
          error: false,
        });
      },
      error: data => {
        this.setState({
          error: true,
        });
      },
    });
  },

  getChartPoints() {
    return this.state.data.map(([x, y]) => {
      return {x, y};
    });
  },

  render() {
    if (this.state.loading) return <LoadingIndicator />;
    else if (this.state.error) return <LoadingError onRetry={this.fetchData} />;

    return (
      <BarChart
        points={this.getChartPoints()}
        className="standard-barchart"
        label={this.props.label}
        height={this.props.height}
      />
    );
  },
});

export default class TeamDashboard extends AsyncView {
  static propTypes = {
    ...AsyncView.propTypes,
    team: PropTypes.object.isRequired,
    onTeamChange: PropTypes.func.isRequired,
  };

  getDefaultState() {
    return {
      since: new Date().getTime() / 1000 - 3600 * 24 * 7,
      resolution: '1h',
    };
  }

  getTitle() {
    return 'Team Dashboard';
  }

  renderBody() {
    let {orgId, teamId} = this.props.params;

    return (
      <div style={{padding: '0 20px'}} className="dashboard">
        <div className="row">
          <div className="col-md-3">
            <Cell>
              <h6>New Issues</h6>
              <strong>1,134</strong>
            </Cell>
          </div>
          <div className="col-md-3">
            <Cell>
              <h6>Events</h6>
              <strong>391,432,134</strong>
            </Cell>
          </div>
          <div className="col-md-3">
            <Cell>
              <h6>Releases</h6>
              <strong>13</strong>
            </Cell>
          </div>
          <div className="col-md-3">
            <Cell>
              <h6>Latest Release</h6>
              <strong>
                1.0.3 <small>(production)</small>
              </strong>
            </Cell>
          </div>
        </div>
        <div className="row">
          <div className="col-md-6">
            <Cell>
              <h6>Events</h6>
              <Chart
                since={this.state.since}
                resolution={this.state.resolution}
                endpoint={`/organizations/${orgId}/stats/`}
                label="events"
              />
            </Cell>
          </div>
          <div className="col-md-6">
            <Cell>
              <h6>Affected Users</h6>
              <Chart
                since={this.state.since}
                resolution={this.state.resolution}
                endpoint={`/organizations/${orgId}/stats/`}
                label="users"
              />
            </Cell>
          </div>
        </div>
        <div className="row">
          <div className="col-md-6">
            <Cell>
              <h6>Releases</h6>
              [...]
            </Cell>
          </div>
          <div className="col-md-6">
            <Cell>
              <h6>Recent Feedback</h6>
              [...]
            </Cell>
          </div>
        </div>
      </div>
    );
  }
}
