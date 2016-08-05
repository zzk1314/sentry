import React from 'react';

import EventDataSection from '../eventDataSection';
import PropTypes from '../../../proptypes';
import utils from '../../../utils';
import {t} from '../../../locale';
import KeyValueList from './keyValueList';

const CommandInterface = React.createClass({
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
          title={t('Command')}>
        <pre className="plain" dangerouslySetInnerHTML={{
          __html: utils.nl2br(utils.urlize(utils.escape(data.output || '')))
        }} />
        <KeyValueList
          data={[
            ['Executable', data.executable],
            ['Arguments', data.args],
            ['Exit Code', data.exitCode],
          ]}
          isContextData={true}
          isSorted={false}
        />
      </EventDataSection>
    );
  }
});

export default CommandInterface;
