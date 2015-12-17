import React from 'react';
import ApiMixin from '../mixins/apiMixin';
import DocumentTitle from 'react-document-title';
import Footer from '../components/footer';
import Header from '../components/header';
import HookStore from '../stores/hookStore';
import LoadingError from '../components/loadingError';
import LoadingIndicator from '../components/loadingIndicator';
import PropTypes from '../proptypes';
import TeamStore from '../stores/teamStore';
import {t} from '../locale';

let ERROR_TYPES = {
  ORG_NOT_FOUND: 'ORG_NOT_FOUND'
};

const OrganizationDetails = React.createClass({
  childContextTypes: {
    organization: PropTypes.Organization
  },

  mixins: [
    ApiMixin
  ],

  getInitialState() {
    return {
      loading: true,
      error: false,
      errorType: null,
      organization: null
    };
  },

  getChildContext() {
    return {
      organization: this.state.organization
    };
  },

  componentWillMount() {
    this.fetchData();
  },

  componentWillReceiveProps(nextProps) {
    if (nextProps.params.orgId !== this.props.params.orgId) {
      this.remountComponent();
    }
  },

  componentWillUnmount() {
    TeamStore.reset();
  },

  remountComponent() {
    this.setState(this.getInitialState(), this.fetchData);
  },

  fetchData() {
    this.api.request(this.getOrganizationDetailsEndpoint(), {
      success: (data) => {
        // Allow injection via getsentry et all
        let hooks = [];
        HookStore.get('organization:header').forEach((cb) => {
          hooks.push(cb(data));
        });

        this.setState({
          organization: data,
          loading: false,
          error: false,
          errorType: null,
          hooks: hooks,
        });

        TeamStore.loadInitialData(data.teams);
      }, error: (_, textStatus, errorThrown) => {
        let errorType = null;
        switch (errorThrown) {
          case 'NOT FOUND':
            errorType = ERROR_TYPES.ORG_NOT_FOUND;
            break;
          default:
        }
        this.setState({
          loading: false,
          error: true,
          errorType: errorType,
        });
      }
    });
  },

  getOrganizationDetailsEndpoint() {
    return '/organizations/' + this.props.params.orgId + '/';
  },

  getTitle() {
    if (this.state.organization)
      return this.state.organization.name;
    return 'Sentry';
  },

  render() {
    if (this.state.loading) {
        return (
          <LoadingIndicator triangle={true}>
            {t('Loading data for your organization.')}
          </LoadingIndicator>
        );
    } else if (this.state.error) {
      switch (this.state.errorType) {
        case ERROR_TYPES.ORG_NOT_FOUND:
          return (
            <div className="container">
              <div className="alert alert-block">
                {t('The organization you were looking for was not found.')}
              </div>
            </div>
          );
        default:
          return <LoadingError onRetry={this.remountComponent} />;
      }
    }

    let params = this.props.params;

    return (
      <DocumentTitle title={this.getTitle()}>
        <div className="app">
          <div className="global-sidebar">
            <a href="" className="logo"><span className="icon-sentry-logo" /></a>
            <hr />
            <ul>
              <li>
                <a href="#">
                  <span className="icon-user" />
                  <span className="badge">12</span>
                </a>
              </li>
              <li><a href="#"><span className="icon-bookmark-2" /></a></li>
              <li><a href="#"><span className="icon-av_timer" /></a></li>
            </ul>
            <hr />
            <div className="global-sidebar-user-nav">
              <ul>
                <li><a href="#"><span className="icon-question"/></a></li>
                <li><a href="#"><span className="icon-globe" /></a></li>
                <li className="dropdown">
                  <a href="#" className="dropdown-toggle">
                    <img src="https://github.com/ckj.png" />
                  </a>
                </li>
              </ul>
            </div>
          </div>
          {this.state.hooks}
          <Header orgId={params.orgId}/>
          {this.props.children}
          <Footer />
        </div>
      </DocumentTitle>
    );
  }
});

export default OrganizationDetails;
