import {Link} from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import styled, {css} from 'react-emotion';

import ExternalLink from '../externalLink';
import InlineSvg from '../inlineSvg';

import '../../../less/components/button.less';

class UnstyledButton extends React.Component {
  static propTypes = {
    priority: PropTypes.oneOf(['primary', 'danger', 'link', 'success']),
    size: PropTypes.oneOf(['zero', 'small', 'xsmall', 'large']),
    disabled: PropTypes.bool,
    busy: PropTypes.bool,
    /**
     * Use this prop if button is a react-router link
     */
    to: PropTypes.string,
    /**
     * Use this prop if button should use a normal (non-react-router) link
     */
    href: PropTypes.string,
    icon: PropTypes.string,
    iconOnly: PropTypes.bool,
    /**
     * Tooltip text
     */
    title: PropTypes.string,
    /**
     * Is an external link? (Will open in new tab)
     */
    external: PropTypes.bool,
    borderless: PropTypes.bool,
    onClick: PropTypes.func,
  };

  static defaultProps = {
    disabled: false,
  };

  // Intercept onClick and propagate
  handleClick = (...args) => {
    let {disabled, busy, onClick} = this.props;

    // Don't allow clicks when disabled or busy
    if (disabled || busy) return;

    if (typeof onClick !== 'function') return;

    onClick(...args);
  };

  getUrl = () => {
    let {disabled, to, href} = this.props;
    if (disabled) return null;
    return to || href;
  };

  render() {
    let {
      priority,
      size,
      to,
      href,
      children,
      className,
      disabled,
      busy,
      title,
      borderless,
      icon,
      external,
      iconOnly,

      // destructure from `buttonProps`
      // not necessary, but just in case someone re-orders props
      // eslint-disable-next-line no-unused-vars
      onClick,
      ...buttonProps
    } = this.props;

    let childContainer = (
      <ButtonLabel size={size} iconOnly={iconOnly}>
        {icon && (
          <IconContainer size={size} iconOnly={iconOnly}>
            <StyledInlineSvg src={icon} size={size === 'small' ? '12px' : '16px'} />
          </IconContainer>
        )}
        {children}
      </ButtonLabel>
    );

    // Buttons come in 3 flavors: Link, anchor, and regular buttons. Let's
    // use props to determine which to serve up, so we don't have to think
    // about it. As a bonus, let's ensure all buttons appear as a button
    // control to screen readers. Note: you must still handle tabindex manually.

    // Props common to all elements

    let componentProps = {
      disabled,
      ...buttonProps,
      onClick: this.handleClick,
      className: classNames(className, {tip: !!title}),
      role: 'button',
      children: childContainer,
      borderless,
      priority,
      size,
      busy,
    };

    // Handle react-router Links
    if (to) {
      return <Link to={this.getUrl()} {...componentProps} />;
    }

    if (href && external) {
      return <ExternalLink href={this.getUrl()} {...componentProps} />;
    }

    // Handle traditional links
    if (href) {
      return <a href={this.getUrl()} {...componentProps} />;
    }

    // Otherwise, fall back to basic button element
    return <button {...componentProps} />;
  }
}

const getTheme = ({priority, theme}) => {
  return {
    primary: {
      background: theme.purple,
      border: theme.purpleDark,
    },
    danger: {
      background: theme.red,
      border: theme.redDark,
    },
    success: {
      background: theme.greenDark,
      border: theme.greenLight,
    },
    link: {
      background: 'transparent',
      border: 'none',
      textColor: theme.blue,
    },
    default: {
      background: '#fff',
      border: theme.gray1,
      textColor: theme.textColor,
    },
  }[priority];
};

const getButtonTheme = ({priority, disabled, theme}) => {
  const button = getTheme({
    priority: disabled && priority !== 'link' ? 'default' : priority || 'default',
    theme,
  });

  return `
    color: ${button.textColor || '#fff'};
    background: ${button.background};
    border: 1px solid ${button.border};
    &:hover,
    &:focus,
    &:active {
      color: ${button.textColor || '#fff'};
      background: ${button.background};
      border-color: ${button.border};
    }
  `;
};

const getFontSize = ({size, theme}) => {
  switch (size) {
    case 'xsmall':
      return theme.fontSizeXSmall;
    case 'small':
      return theme.fontSizeSmall;
    case 'large':
      return theme.fontSizeMedium;
    default:
      return theme.fontSizeButton;
  }
};

const Button = styled(UnstyledButton)`
  display: inline-block;
  line-height: 1;
  font-weight: ${p => p.isLink ? 400 : 600};
  border-radius: 3px;
  box-shadow: ${p => (p => p.isLink || p.isDisabled ? '0 2px rgba(0, 0, 0, 0.05)' : 'none')};
  cursor: ${p => (p.isDisabled ? 'not-allowed' : 'pointer')};
  font-size: ${p => getFontSize(p)};
  padding: 0;
  text-transform: none;

  ${p => getButtonTheme(p)};

  opacity: ${p => (p.busy || p.disabled ? 0.65 : 1)};
`;

const getPadding = ({iconOnly, size, priority}) => {
  if (size == 'zero' || priority == 'link') return 0;
  return iconOnly ? '0.5em' : '0.5em 0.75em';
};

const ButtonLabel = styled('div')`
  padding: ${p => getPadding(p)};
  display: flex;
  align-items: center;
`;

const IconContainer = styled('div')`
  margin-right: ${p => (p.iconOnly ? 0 : '0.5em')};
  margin-left: ${p => (p.iconOnly ? 0 : '-2px')};
`;

const StyledInlineSvg = styled(InlineSvg)`
  display: block;
`;

export default Button;
