import React from 'react';

import AsyncView from './asyncView';
import DropdownLink from '../components/dropdownLink';
import IndicatorStore from '../stores/indicatorStore';
import MenuItem from '../components/menuItem';
import OrganizationHomeContainer from '../components/organizations/homeContainer';
import {t} from '../locale';

export default class IntegrationDetails extends AsyncView {
  getEndpoints() {
    let {integrationId, orgId} = this.props.params;
    return [['integration', `/organizations/${orgId}/integrations/${integrationId}/`]];
  }

  getTitle() {
    return 'Integrations';
  }

  renderBody() {
    let {integration} = this.state;
    return (
      <OrganizationHomeContainer>
        <div className="ref-integration-details">
          <h3 className="m-b-2">
            {integration.provider.name}
            <small style={{marginLeft: 10}}>
              {integration.name}
            </small>
          </h3>
          <p>
            This is where we'll explain what this integration let's you do, and provide
            any additional global configuration.
          </p>
        </div>
      </OrganizationHomeContainer>
    );
  }
}
