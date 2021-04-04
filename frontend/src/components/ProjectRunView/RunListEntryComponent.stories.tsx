import { Meta, Story } from "@storybook/react";
import React from "react";
import RunListEntryComponent from "./RunListEntryComponent";
import { RunStatusDto } from "../../catoapimodels";
import { HashRouter } from "react-router-dom";

export default {
  title: "RunListEntryComponent",
  component: RunListEntryComponent,
} as Meta;

interface Args {
  isCurrentEntry: boolean;
  status: RunStatusDto;
}

const Template: Story<Args> = (args) => (
  <HashRouter>
    <RunListEntryComponent
      run={{
        id: 1,
        project_id: 2,
        started_at: new Date().toISOString(),
        status: args.status,
      }}
      isCurrentEntry={args.isCurrentEntry}
      link={"/some/link"}
    />
  </HashRouter>
);

export const Running = Template.bind({});
Running.args = { isCurrentEntry: false, status: RunStatusDto.RUNNING };

export const Success = Template.bind({});
Success.args = { isCurrentEntry: false, status: RunStatusDto.SUCCESS };

export const NotStarted = Template.bind({});
NotStarted.args = { isCurrentEntry: false, status: RunStatusDto.NOT_STARTED };

export const Failed = Template.bind({});
Failed.args = { isCurrentEntry: false, status: RunStatusDto.FAILED };
