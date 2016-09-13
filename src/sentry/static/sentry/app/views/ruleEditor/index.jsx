import React from 'react';
import ReactDOM from 'react-dom';
import {History} from 'react-router';
import jQuery from 'jquery';

import ApiMixin from '../../mixins/apiMixin';
import IndicatorStore from '../../stores/indicatorStore';
import SelectInput from '../../components/selectInput';
import {t} from '../../locale';

import RuleNodeList from './ruleNodeList';

const RuleEditor = React.createClass({
  propTypes: {
    config: React.PropTypes.object.isRequired,
    rule: React.PropTypes.object.isRequired,
    projectId: React.PropTypes.string.isRequired,
    orgId: React.PropTypes.string.isRequired
  },

  mixins: [
    ApiMixin,
    History
  ],

  getInitialState() {
    let rule = this.props.rule;
    return {
      loading: false,
      error: null,
      actions: rule.actions,
      conditions: rule.conditions,
    };
  },

  componentDidUpdate() {
    if (this.state.error) {
      jQuery(document.body).scrollTop(jQuery(ReactDOM.findDOMNode(this.refs.form)).offset().top);
    }
  },

  onActionsChange(data) {
    this.setState({actions: data});
  },

  onConditionsChange(data) {
    this.setState({conditions: data});
  },

  onSubmit(e) {
    e.preventDefault();
    let actionMatch = $(ReactDOM.findDOMNode(this.refs.actionMatch)).val();
    let name = $(ReactDOM.findDOMNode(this.refs.name)).val();
    let data = {
      actionMatch: actionMatch,
      actions: this.state.actions,
      conditions: this.state.conditions,
      name: name
    };
    let rule = this.props.rule;
    let projectId = this.props.projectId;
    let orgId = this.props.orgId;
    let endpoint = `/projects/${orgId}/${projectId}/rules/`;
    if (rule.id) {
      endpoint += rule.id + '/';
    }

    let loadingIndicator = IndicatorStore.add('Saving...');
    this.api.request(endpoint, {
      method: (rule.id ? 'PUT' : 'POST'),
      data: data,
      success: () => {
        this.history.pushState(null, `/${orgId}/${projectId}/settings/alerts/rules/`, {});
      },
      error: (response) => {
        this.setState({
          error: response.responseJSON || {'__all__': 'Unknown error'},
          loading: false
        });
      },
      complete: () => {
        IndicatorStore.remove(loadingIndicator);
      }
    });
  },

  hasError(field) {
    let {error} = this.state;
    if (!error) return false;
    return !!error[field];
  },

  render() {
    let {rule, config} = this.props;
    let {loading, error} = this.state;
    let {actionMatch, actions, conditions, name} = rule;

    return (
      <div ref="form">
        <div className="box rule-detail">
          <div className="box-header">
            <h3>
              {rule.id ? 'Edit Alert Rule' : 'New Alert Rule'}
            </h3>
          </div>
          <div className="box-content with-padding">
            {error &&
              <div className="alert alert-block alert-error">
                <p>{t('There was an error saving your changes. Make sure all fields are valid and try again.')}</p>
              </div>
            }
            <h6>{t('Rule name')}:</h6>
            <div className="control-group">
              <input ref="name"
                     type="text" className="form-control"
                     defaultValue={name}
                     required={true}
                     placeholder={t('My Rule Name')} />
            </div>

            <div className="node-match-selector">
              <h6>
                {t('Every time %s of these conditions are met:',
                  <SelectInput ref="actionMatch"
                        className={(this.hasError('actionMatch') ? ' error' : '')}
                        value={actionMatch}
                        style={{width:80}}
                        required={true}>
                    <option value="all">{t('all')}</option>
                    <option value="any">{t('any')}</option>
                    <option value="none">{t('none')}</option>
                  </SelectInput>
                )}
              </h6>
            </div>

            {this.hasError('conditions') &&
              <p className="error">{t('Ensure at least one condition is enabled and all required fields are filled in.')}</p>
            }

            <RuleNodeList nodes={config.conditions}
              initialItems={conditions}
              className="rule-condition-list"
              onChange={this.onConditionsChange} />

            <h6>{t('Take these actions:')}</h6>

            {this.hasError('actions') &&
              <p className="error">{t('Ensure at least one action is enabled and all required fields are filled in.')}</p>
            }

            <RuleNodeList nodes={config.actions}
              initialItems={actions}
              className="rule-action-list"
              onChange={this.onActionsChange} />

            <div className="actions">
              <button className="btn btn-primary btn-lg"
                      onClick={this.onSubmit}
                      disabled={loading}>{t('Save Rule')}</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
});

export default RuleEditor;
