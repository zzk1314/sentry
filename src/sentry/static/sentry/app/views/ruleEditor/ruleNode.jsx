import React from 'react';
import jQuery from 'jquery';
import _ from 'underscore';

import {BooleanField, EmailField, NumberField, PasswordField, Select2Field, TextField} from '../../components/forms';

const RuleNode = React.createClass({
  propTypes: {
    data: React.PropTypes.object.isRequired,
    node: React.PropTypes.shape({
      id: React.PropTypes.string.isRequired,
      config: React.PropTypes.array.isRequired,
      nameRaw: React.PropTypes.string.isRequired,
    }).isRequired,
    onDelete: React.PropTypes.func.isRequired
  },

  componentDidMount() {
    let $html = jQuery(this.refs.html);

    $html.find('select, input, textarea').each((_1, el) => {
      let $el = $(el);
      $el.attr('id', '');
      $el.val(this.props.data[el.name]);
    });

    $html.find('select').select2();

    $html.find('input.typeahead').each((_1, el) => {
      let $el = $(el);
      $el.select2({
        initSelection: function(option, callback) {
          let $option = $(option);
          callback({id: $option.val(), text: $option.val()});
        },
        data: $el.data('choices'),
        createSearchChoice: function(term) {
          return {id: $.trim(term), text: $.trim(term)};
        }
      });
    });
  },

  getField(config) {
    switch (config.type) {
      case 'secret':
        return PasswordField;
      case 'bool':
        return BooleanField;
      case 'email':
        return EmailField;
      case 'string':
      case 'text':
      case 'url':
        return TextField;
      case 'number':
        return NumberField;
      case 'choice':
      case 'select':
        return Select2Field;
      default:
        return null;
    }
  },

  formattedName() {
    let node = this.props.node;
    return node.nameRaw.split(' ').map((p, idx) => {
      let m = p.match(/^{([^\}]+)\}$/);
      if (!m) return <span key={idx}>{p} </span>;
      let fieldConfig = _.find(node.config, f => f.name === m[1]);
      if (!fieldConfig) return <span key={idx}>{p} </span>;
      let field = new (this.getField(fieldConfig))(fieldConfig);
      return <span key={idx}>{field.getField()}</span>;
    });
  },

  render() {
    let data = this.props.data;
    return (
      <tr>
        <td className="rule-form">
          <input type="hidden" name="id" value={data.id} />
          <span ref="html">{this.formattedName()}</span>
        </td>
        <td className="align-right">
          <a onClick={this.props.onDelete}>
            <span className="icon-trash" />
          </a>
        </td>
      </tr>
    );
  }
});

export default RuleNode;
