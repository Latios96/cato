interface ImageChannel{
    id: number,
    image_id: number,
    name: string,
    file_id: string
}

export default interface Image{
    id: number,
    name: string,
    original_file_id: string
    channels: ImageChannel[]
}

