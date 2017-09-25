import PropTypes from 'prop-types';
import React from 'react';
import {Link} from 'react-router';

import ApiMixin from '../mixins/apiMixin';
import Count from './count';
import EventOrGroupTitle from './eventOrGroupTitle';
import TimeSince from './timeSince';

export default React.createClass({
  propTypes: {
    orgId: PropTypes.string.isRequired
  },

  mixins: [ApiMixin],

  render() {
    return <div>This is a selector for notification destinations.</div>;
  }
});
