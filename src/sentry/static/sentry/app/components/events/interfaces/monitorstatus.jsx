import React from 'react';

import EventDataSection from '../eventDataSection';
import PropTypes from '../../../proptypes';
import {t} from '../../../locale';
import KeyValueList from './keyValueList';

const MonitorStatusInterface = React.createClass({
  propTypes: {
    group: PropTypes.Group.isRequired,
    event: PropTypes.Event.isRequired,
    type: React.PropTypes.string.isRequired,
    data: React.PropTypes.object.isRequired,
  },

  render() {
    let data = this.props.data;
    return (
      <EventDataSection
          group={this.props.group}
          event={this.props.event}
          type="command"
          title={t('Monitor')}>
        <KeyValueList
          data={[
            ['ID', data.monitorId],
            ['Label', data.label],
            ['Status', data.status],
          ]}
          isContextData={true}
          isSorted={false}
        />
      </EventDataSection>
    );
  }
});

export default MonitorStatusInterface;
