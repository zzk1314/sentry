/*eslint react/jsx-key:0*/
import PropTypes from 'prop-types';

import React from 'react';
import _ from 'lodash';

import Avatar from '../../../components/avatar';
import KeyValueList from '../interfaces/keyValueList';

class UserContextType extends React.Component {
  static propTypes = {
    data: PropTypes.object.isRequired,
    groupId: PropTypes.string.isRequired,
    orgId: PropTypes.string.isRequired,
    projectId: PropTypes.string.isRequired,
  };

  render() {
    let {groupId, projectId, orgId} = this.props;
    let user = this.props.data;
    let builtins = [];
    let children = [];

    // Handle our native attributes special
    user.id && builtins.push(['ID', <pre>{user.id}</pre>]);
    user.email &&
      builtins.push([
        'Email',
        <pre>
          {user.email}
          <a href={`mailto:${user.email}`} target="_blank" className="external-icon">
            <em className="icon-envelope" />
          </a>
        </pre>,
      ]);
    user.username && builtins.push(['Username', <pre>{user.username}</pre>]);
    user.ip_address && builtins.push(['IP Address', <pre>{user.ip_address}</pre>]);
    user.name && builtins.push(['Name', <pre>{user.name}</pre>]);

    if (user.location) {
      let url =
        `/${orgId}/${projectId}/issues/${groupId}/geo/?highlight=` +
        encodeURIComponent(user.location);
      let location = (
        <span>
          {user.location}
          <a key="external" href={url} className="external-icon">
            <em className="icon-open" />
          </a>
        </span>
      );
      builtins.push(['Location', location]);
    }

    // We also attach user supplied data as 'user.data'
    _.each(user.data, function(value, key) {
      children.push([key, value]);
    });

    return (
      <div className="user-widget">
        <div className="pull-left">
          <Avatar user={user} size={96} gravatar={false} />
        </div>
        <table className="key-value table">
          <tbody>
            {builtins.map(([key, value]) => {
              return (
                <tr key={key}>
                  <td className="key" key="0">
                    {key}
                  </td>
                  <td className="value" key="1">
                    {value}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {children && <KeyValueList data={children} isContextData={true} />}
      </div>
    );
  }
}

UserContextType.getTitle = function(value) {
  return 'User';
};

export default UserContextType;
