import React, { ReactElement } from "react";
import styles from "./PopoverMenu.module.scss";

import { OverlayTrigger } from "react-bootstrap";
import { joinClassnames } from "../../utils/classnameUtils";
import { isNotLast } from "../../utils/arrayUtils";

interface MenuItem {
  id: string;
  element: JSX.Element;
  onClick?: () => void;
}
interface Props {
  id: string;
  menuItems: MenuItem[];
  menuTriggerElement: ReactElement;
}
function PopoverMenu(props: Props) {
  return (
    <OverlayTrigger
      placement="bottom"
      trigger={"click"}
      rootClose={true}
      overlay={
        <div className={styles.inputContainer}>
          {props.menuItems.map((menuItem, i) => {
            const classNames = joinClassnames([
              styles.menuItem,
              menuItem.onClick && styles.menuItemClickable,
              isNotLast(i, props.menuItems) && styles.menuItemBorder,
            ]);
            return (
              <div
                id={props.id + "-" + menuItem.id}
                className={classNames}
                onClick={menuItem.onClick}
              >
                {menuItem.element}
              </div>
            );
          })}
        </div>
      }
    >
      {props.menuTriggerElement}
    </OverlayTrigger>
  );
}

export default PopoverMenu;
