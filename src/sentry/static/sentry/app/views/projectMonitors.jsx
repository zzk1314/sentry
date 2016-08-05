import React from 'react';

import ApiMixin from '../mixins/apiMixin';
import LoadingError from '../components/loadingError';
import LoadingIndicator from '../components/loadingIndicator';
import DateTime from '../components/dateTime';
import {t} from '../locale';

const ProjectMonitors = React.createClass({
  mixins: [ApiMixin],

  getInitialState() {
    return {
      loading: true,
      error: false,
      monitors: [],
    };
  },

  componentDidMount() {
    this.fetchData();
  },

  fetchData() {
    let {orgId, projectId} = this.props.params;
    this.api.request(`/projects/${orgId}/${projectId}/monitors/`, {
      success: (data, _, jqXHR) => {
        this.setState({
          error: false,
          loading: false,
          monitors: data,
          pageLinks: jqXHR.getResponseHeader('Link')
        });
      },
      error: () => {
        this.setState({
          error: true,
          loading: false
        });
      }
    });
  },

  renderDebugTable() {
    let body;

    if (this.state.loading)
      body = this.renderLoading();
    else if (this.state.error)
      body = <LoadingError onRetry={this.fetchData} />;
    else if (this.state.monitors.length > 0)
      body = this.renderResults();
    else
      body = this.renderEmpty();

    return body;
  },

  renderLoading() {
    return (
      <div className="box">
        <LoadingIndicator />
      </div>
    );
  },

  renderEmpty() {
    return (
      <div className="box empty-stream">
        <span className="icon icon-exclamation" />
        <p>{t('There are no monitors for this project.')}</p>
      </div>
    );
  },

  renderResults() {
    return (
      <table className="table">
        <thead>
          <tr>
            <th>{t('Label')}</th>
            <th>{t('Date Added')}</th>
            <th>{t('Status')}</th>
          </tr>
        </thead>
        <tbody>
          {this.state.monitors.map((item, idx) => {
            return (
              <tr key={idx}>
                <td>{item.label}</td>
                <td><DateTime date={item.dateAdded}/></td>
                <td>{item.status === 0 ? 'healthy' : 'unhealthy'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    );
  },

  render() {
    return (
      <div>
        <h1>{t('Monitors')}</h1>
        <p>{t(`
          An overview over the monitors that exist for your project.
        `)}</p>
        {this.renderDebugTable()}
      </div>
    );
  }
});

export default ProjectMonitors;
