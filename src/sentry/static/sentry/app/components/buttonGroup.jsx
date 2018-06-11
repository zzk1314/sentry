import React from 'react';
import styled from 'react-emotion';
import {Flex} from 'grid-emotion';

export default class ButtonGroup extends React.Component {
  render() {
    return <StyledButtonGroup {...this.props} />;
  }
}

// This is so we can use this as a selector in other components (e.g. <Button>)
const StyledButtonGroup = styled(Flex)``;
export {StyledButtonGroup};
