import React from 'react';
import Avatar from '../../components/avatar';
import TimeSince from '../../components/timeSince';
import {nl2br, urlize, escape} from '../../utils';


const EventUserReport = React.createClass({
  propTypes: {
    event: React.PropTypes.object.isRequired
  },

  render() {
    let report = this.props.event.userReport;

    return (
      <div className="user-report">
        <div className="activity-container">
          <ul className="activity">
            <li className="activity-note">
              <Avatar user={report} size={64} className="avatar" />
              <div className="activity-bubble">
                <TimeSince date={report.dateCreated} />
                <div className="activity-author">{report.name} <small>{report.email}</small></div>
                <p dangerouslySetInnerHTML={{__html: nl2br(urlize(escape(report.comments)))}} />
              </div>
            </li>
          </ul>
        </div>
      </div>
    );
  }
});

export default EventUserReport;
