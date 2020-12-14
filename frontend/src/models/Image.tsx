import ImageChannel from "./ImageChannel";

export default interface Image {
  id: number;
  name: string;
  original_file_id: string;
  channels: ImageChannel[];
}
