import React from 'react';

import {FormState, GenericField} from '../../components/forms';

const RuleNode = React.createClass({
  propTypes: {
    data: React.PropTypes.object.isRequired,
    node: React.PropTypes.shape({
      nameRaw: React.PropTypes.string.isRequired
    }).isRequired,
    onChange: React.PropTypes.func.isRequired,
    onDelete: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    return {
      formState: new FormState({
        initial: this.props.data.data,
        onChange: this.onFormStateChange,
      }),
    };
  },

  onFormStateChange(data) {
    this.props.onChange(data);
  },

  formattedName() {
    let node = this.props.node;
    return node.nameRaw;
    // let data = this.state.formState.data;
    // return node.nameRaw.replace(/\{([^\}]+)\}/g, (m, name) => {
    //   return data.hasOwnProperty(name) ? data[name] : `{${name}}`;
    // });
  },

  render() {
    let {node} = this.props;
    return (
      <li>
        <div className="pull-right">
          <a onClick={this.props.onDelete}>
            <span className="icon-trash" />
          </a>
        </div>
        <h6>{this.formattedName()}</h6>
        {node.config.length !== 0 &&
          <form className="form-inline rule-form">
            {node.config.map(f => {
              return (
                <GenericField
                  key={f.name}
                  config={f}
                  state={this.state.formState} />
              );
            })}
          </form>
        }
      </li>
    );
  }
});

export default RuleNode;
