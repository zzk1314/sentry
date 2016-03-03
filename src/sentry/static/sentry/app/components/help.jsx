import React from 'react';
import jQuery from 'jquery';
import {t} from '../locale';

const RIGIDSEARCH = 'https://rigidsearch.getsentry.net/api/search';

const Help = React.createClass({
  propTypes: {
  },

  getInitialState() {
    return {
      results: null,
      loading: false
    };
  },

  onSearchKeyUp(e) {
    this.setState({loading: true});
    this.xhr && this.xhr.abort();
    this.xhr = jQuery.ajax({
      type: 'GET',
      url: RIGIDSEARCH,
      data: {
        q: e.target.value,
        page: 1,
        section: 'hosted'
      },
      crossDomain: true,
      cache: true,
      success: (data) => {
        this.setState({
          loading: false,
          results: data
        });
      },
      error: () => {
        this.setState({
          loading: false,
          results: null
        });
      }
    });
  },

  render() {
    let className = this.props.className || 'help-container';
    let results = this.state.results;
    return (
      <div className={className}>
        <div className="bubble dropdown open">{t('Halp')}
          <ul className="dropdown-menu dropdown-menu-right">
            {results && results.items && results.items.length && results.items.map((item, i) => {
              return (
                <li key={i} dangerouslySetInnerHTML={{__html: item.excerpt}} />
              );
            }) || <li>{t('No results')}</li>}
            <li>
              <input className="form-control" type="text" placeholder={t('What can I help you with?')} onKeyUp={this.onSearchKeyUp} />
            </li>
          </ul>
        </div>
      </div>
    );
  }
});

export default Help;
