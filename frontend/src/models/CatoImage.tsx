import ImageChannel from "./ImageChannel";

export default interface CatoImage {
  id: number;
  name: string;
  original_file_id: string;
  channels: ImageChannel[];
}
