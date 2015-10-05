import DocumentTitle from "react-document-title";
import React from "react";
import Router from "react-router";

import Footer from "../../components/footer";
import Header from "../../components/header";
import ListLink from "../../components/listLink";

const Admin = React.createClass({
  contextTypes: {
    router: React.PropTypes.func
  },

  getTitle() {
    return 'Sentry Admin';
  },

  render() {
    return (
      <DocumentTitle title={this.getTitle()}>
        <div className="app">
          <Header />
          <div className="container">
            <div className="content">
              <div className="row">
                <div className="col-md-2">
                  <h6 className="nav-header">System</h6>
                  <ul className="nav nav-stacked">
                    <ListLink to="adminOverview">Overview</ListLink>
                  </ul>

                  <h6 className="nav-header">Manage</h6>
                  <ul className="nav nav-stacked">
                  </ul>
                </div>
                <div className="col-md-10">
                  <Router.RouteHandler />
                </div>
              </div>
            </div>
          </div>
          <Footer />
        </div>
      </DocumentTitle>
    );
  }
});

export default Admin;
