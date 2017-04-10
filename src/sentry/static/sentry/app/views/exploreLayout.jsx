import React from 'react';
import ListLink from '../components/listLink';
import OrganizationState from '../mixins/organizationState';
import ProjectSelector from '../components/projectHeader/projectSelector';
import TooltipMixin from '../mixins/tooltip';
import {t} from '../locale';

export default React.createClass({
  mixins: [
    OrganizationState,
    TooltipMixin({
      selector: '.tip'
    })
  ],

  render() {
    let org = this.getOrganization();
    let access = this.getAccess();

    let orgId = org.slug;

    return (
      <div className="organization-home">
        <div className="sub-header flex flex-container flex-vertically-centered">
          <ProjectSelector
              organization={org} />
        </div>
        <div className="container">
          <div className="content row">
            <div className="col-md-2 org-sidebar">
              <h6 className="nav-header">{t('Audience')}</h6>
              <ul className="nav nav-stacked">
                <ListLink to={`/organizations/${orgId}/explore/audience/`}>{t('Overview')}</ListLink>
                <ListLink to={`/organizations/${orgId}/explore/audience/devices/`}>{t('Devices')}</ListLink>
                <ListLink to={`/organizations/${orgId}/explore/audience/browsers/`}>{t('Browsers')}</ListLink>
                <ListLink to={`/organizations/${orgId}/explore/audience/browsers/`}>{t('Transactions')}</ListLink>
              </ul>
              <h6 className="nav-header">{t('Users')}</h6>
              <ul className="nav nav-stacked">
                <ListLink to={`/organizations/${orgId}/explore/users/`}>{t('Overview')}</ListLink>
                <ListLink to={`/organizations/${orgId}/explore/users/geo/`}>{t('Geo')}</ListLink>
                <ListLink to={`/organizations/${orgId}/explore/users/language/`}>{t('Language')}</ListLink>
              </ul>
            </div>
            <div className="col-md-10">
              {this.props.children}
            </div>
          </div>
        </div>
      </div>
    );
  }
});
