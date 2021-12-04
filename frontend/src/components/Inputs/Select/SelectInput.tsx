import { OverlayTrigger } from "react-bootstrap";
import React, { useCallback, useState } from "react";
import ArrowButton from "../../Button/ArrowButton";
import styles from "./SelectInput.module.scss";
import { CheckLg } from "react-bootstrap-icons";
interface Props {
  title: string;
  subtitle?: string;
  elements: string[];
  onChange?: (selectedElements: Set<string>) => void;
  selectedElements?: Set<string>;
}
export function SelectInput(props: Props) {
  const [selectedElements, setSelectedElements] = useState<Set<string>>(
    props.selectedElements || new Set()
  );

  const handleClick = useCallback(
    (element: string) => {
      const newSelectedElements = new Set(selectedElements);
      if (selectedElements.has(element)) {
        newSelectedElements.delete(element);
      } else {
        newSelectedElements.add(element);
      }
      if (props.onChange) {
        props.onChange(newSelectedElements);
      }
      setSelectedElements(newSelectedElements);
    } /*eslint-disable-next-line react-hooks/exhaustive-deps*/,
    [props.onChange, selectedElements, setSelectedElements]
  );

  return (
    <OverlayTrigger
      placement="bottom"
      trigger={"click"}
      rootClose={true}
      overlay={
        <div className={styles.inputContainer}>
          {props.subtitle ? (
            <div className={styles.subtitle}>{props.subtitle}</div>
          ) : null}
          <div className={styles.elementsContainer}>
            {props.elements.map((element) => {
              return (
                <div
                  className={styles.inputElement}
                  onClick={() => handleClick(element)}
                  key={element}
                >
                  <span
                    data-testid={
                      selectedElements.has(element)
                        ? element + "-selected"
                        : undefined
                    }
                  >
                    {selectedElements.has(element) ? (
                      <CheckLg size={20} />
                    ) : null}
                  </span>
                  <span>{element}</span>
                </div>
              );
            })}
          </div>
        </div>
      }
    >
      <ArrowButton text={props.title} direction={"down"} />
    </OverlayTrigger>
  );
}
