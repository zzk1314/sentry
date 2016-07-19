import React from 'react';
import queryString from 'query-string';

import KeyValueList from './keyValueList';
import ContextData from '../../contextData';
import Truncate from '../../truncate';
import {objectIsEmpty} from '../../../utils';
import {t} from '../../../locale';

const RichHttpContent = React.createClass({
  propTypes: {
    data: React.PropTypes.object.isRequired
  },

  getInitialState() {
    return {
      expanded: false,
    };
  },

  /**
   * Converts an object of body/querystring key/value pairs
   * into a tuple of [key, value] pairs, and sorts them.
   *
   * Note that the query-string parser returns dupes like this:
   *   { foo: ['bar', 'baz'] } // ?foo=bar&bar=baz
   *
   * This method accounts for this.
   */
  objectToSortedTupleArray(obj) {
    return Object.keys(obj).reduce((out, k) => {
      let val = obj[k];
      return out.concat(
        {}.toString.call(val) === '[object Array]' ?
          val.map(v => [k, v]) : // key has multiple values (array)
          [[k, val]]             // key has single value
      );
    }, []).sort(function ([keyA], [keyB]) {
      return keyA < keyB ? -1 : 1;
    });
  },

  getBodySection(data) {
    /*eslint no-empty:0*/
    let contentType = data.headers.find(h => h[0] === 'Content-Type');
    contentType = contentType && contentType[1].split(';')[0].toLowerCase();

    // Ignoring Content-Type, we immediately just check if the body is parseable
    // as JSON. Why? Because many applications don't set proper Content-Type values,
    // e.g. x-www-form-urlencoded  actually contains JSON.
    try {
      return <ContextData data={JSON.parse(data.data)} />;
    } catch (e) {}

    if (contentType === 'application/x-www-form-urlencoded') {
      return this.getQueryStringOrRaw(data.data);
    } else {
      return <pre>{data.data}</pre>;
    }
  },

  getQueryStringOrRaw(data) {
    try {
      // Sentry API abbreviates long query string values, sometimes resulting in
      // an un-parsable querystring ... stay safe kids
      return <KeyValueList data={this.objectToSortedTupleArray(queryString.parse(data))} />;
    } catch (e) {
      return <pre>{data}</pre>;
    }
  },

  onExpand() {
    this.setState({
      expanded: true,
    });
  },

  render(){
    let data = this.props.data;

    let fullUrl = data.url;
    if (data.query) {
      fullUrl = fullUrl + '?' + data.query;
    }
    if (data.fragment) {
      fullUrl = fullUrl + '#' + data.fragment;
    }

    let headers = data.headers || {};

    let moreData = (
      data.query || data.data || data.cookies || data.headers || data.env
    );

    let expanded = this.state.expanded;

    return (
      <div>
        <table className="table key-value">
          <tbody>
            <tr key="method">
              <td className="key">Method</td>
              <td className="value"><pre>{data.method || 'GET'}</pre></td>
            </tr>
            <tr key="url">
              <td className="key">URL</td>
              <td className="value">
                <pre><a href={fullUrl}><Truncate value={fullUrl} maxLength={200} leftTrim={true} /></a></pre>
              </td>
            </tr>
            {data.fragment &&
              <tr key="fragment">
                <td className="key">Fragment</td>
                <td className="value"><pre>{data.fragment}</pre></td>
              </tr>
            }
            {headers.Referer &&
              <tr key="referer">
                <td className="key">Referer</td>
                <td className="value"><pre>{headers.Referer}</pre></td>
              </tr>
            }
            {headers['User-Agent'] &&
              <tr key="referer">
                <td className="key">User-Agent</td>
                <td className="value"><pre>{headers['User-Agent']}</pre></td>
              </tr>
            }
          </tbody>
        </table>
        {moreData &&
          <div>
            <div key="e" className={'expander ' + (expanded && 'expanded')}>
              <span>
                <a onClick={this.onExpand} className="show-more btn btn-primary btn-xs">
                  {t('Show more')}
                </a>
              </span>
            </div>
            <div key="d" style={{display: expanded ? 'block' : 'none'}}>
              <table className="table key-value">
                <tbody>
                {data.query &&
                  <tr key="query">
                    <td className="key">{t('Query String')}</td>
                    <td className="value">{this.getQueryStringOrRaw(data.query)}</td>
                  </tr>
                }
                {data.data &&
                  <tr key="data">
                    <td className="key">{t('Body')}</td>
                    <td className="value">{this.getBodySection(data)}</td>
                  </tr>
                }

                {data.cookies && !objectIsEmpty(data.cookies) &&
                  <tr key="cookies">
                    <td className="key">{t('Cookies')}</td>
                    <td className="value"><ContextData data={data.cookies} /></td>
                  </tr>
                }
                {!objectIsEmpty(headers) &&
                  <tr key="headers">
                    <td className="key">{t('Headers')}</td>
                    <td className="value"><ContextData data={headers} /></td>
                  </tr>
                }
                {!objectIsEmpty(data.env) &&
                  <tr key="env">
                    <td className="key">{t('Environment')}</td>
                    <td className="value"><ContextData data={this.objectToSortedTupleArray(data.env)}/></td>
                  </tr>
                }
                </tbody>
              </table>
            </div>
          </div>
        }
      </div>
    );
  }
});

export default RichHttpContent;
