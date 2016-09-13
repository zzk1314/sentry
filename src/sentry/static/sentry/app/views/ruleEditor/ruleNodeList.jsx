import React from 'react';

import SelectInput from '../../components/selectInput';
import RuleNode from './ruleNode';

const RuleNodeList = React.createClass({
  propTypes: {
    initialItems: React.PropTypes.array,
    nodes: React.PropTypes.array.isRequired,
    onChange: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    return {
      items: this.props.initialItems || [],
    };
  },

  componentWillMount() {
    this._nodesById = {};

    this.props.nodes.forEach((node) => {
      this._nodesById[node.id] = node;
    });
  },

  onAddRow(sel) {
    let nodeId = sel.val();
    if (!nodeId) return;

    sel.val('');

    this.state.items.push({
      id: nodeId,
    });
    this.setState({
      items: this.state.items,
    });
    this.props.onChange(this.state.items);
  },

  onChangeRow(idx, data) {
    this.state.items[idx].data = data;
    this.setState({
      items: this.state.items,
    });
    this.props.onChange(this.state.items);
  },

  onDeleteRow(idx) {
    this.state.items.splice(idx, 1);
    this.setState({
      items: this.state.items,
    });
    this.props.onChange(this.state.items);
  },

  getNode(id) {
    return this._nodesById[id];
  },

  render() {
    return (
      <div className={this.props.className}>
        <ul className="node-list" style={{marginBottom: '10px'}}>
          {this.state.items.map((item, idx) => {
            return (
              <RuleNode
                key={idx}
                node={this.getNode(item.id)}
                onChange={this.onChangeRow.bind(this, idx)}
                onDelete={this.onDeleteRow.bind(this, idx)}
                data={item} />
            );
          })}
        </ul>
        <fieldset className="node-selector">
          <SelectInput onChange={this.onAddRow} style={{width: '100%'}}>
            <option key="blank" />
            {this.props.nodes.map((node) => {
              return (
                <option value={node.id} key={node.id}>{node.nameRaw}</option>
              );
            })}
          </SelectInput>
        </fieldset>
      </div>
    );
  }
});

export default RuleNodeList;
