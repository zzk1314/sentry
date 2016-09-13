import React from 'react';

import {
  Form,
  FormState,
  GenericField
} from '../../components/forms';
import {Client} from '../../api';
import LoadingIndicator from '../../components/loadingIndicator';

class PluginSettings extends React.Component {
  constructor(props) {
    super(props);

    this.onSubmit = this.onSubmit.bind(this);
    this.fetchData = this.fetchData.bind(this);

    this.state = {
      fieldList: null,
      loading: true,
      error: false,
      formState: new FormState(),
    };
  }

  componentWillMount() {
    this.api = new Client();
  }

  componentDidMount() {
    this.fetchData();
  }

  componentWillUnmount() {
    this.api.clear();
  }

  getPluginEndpoint() {
    let org = this.props.organization;
    let project = this.props.project;
    return (
      `/projects/${org.slug}/${project.slug}/plugins/${this.props.plugin.id}/`
    );
  }

  onSubmit(data, success, failure) {
    this.api.request(this.getPluginEndpoint(), {
      data: data,
      method: 'PUT',
      success: () => {
        success();
      },
      error: (error) => {
        failure((error.responseJSON || {}).errors);
      },
    });
  }

  fetchData() {
    this.api.request(this.getPluginEndpoint(), {
      success: (data) => {
        let formData = {};
        data.config.forEach((field) => {
          formData[field.name] = field.value || field.defaultValue;
        });
        this.setState({
          error: false,
          loading: false,
          initialData: formData,
          fieldList: data.config,
        });
      },
      error: (error) => {
        this.setState({
          error: true,
          loading: false,
        });
      }
    });
  }

  render() {
    if (!this.state.fieldList) {
      return <LoadingIndicator />;
    }
    return (
      <Form onSubmit={this.onSubmit} initial={this.state.initialData}>
        {this.state.fieldList.map(f => <GenericField key={f.name} config={f} />)}
      </Form>
    );
  }
}

PluginSettings.propTypes = {
    organization: React.PropTypes.object.isRequired,
    project: React.PropTypes.object.isRequired,
    plugin: React.PropTypes.object.isRequired,
};

export default PluginSettings;
