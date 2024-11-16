"use client";
import Image from "next/image";
import { useEffect, useState } from "react";
import useSWR from "swr";
import { Tweet } from "react-tweet";
import Map, { Marker } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";

type Content = {
  id: string;
  content: string;
  tweet_url: string | null;
  lat: number | null;
  lng: number | null;
  ek_agent_url: string | null;
  timestamp: string;
};

const fetcher = (...args: [string, ...any[]]) =>
  fetch(...args).then((res) => res.json());

const getTweetId = (url: string | undefined) => {
  if (!url) return undefined;
  const match = url.match(/\/status\/(\d+)/);
  return match ? match[1] : undefined;
};

function ContentCard({ content }: { content: Content }) {
  const tweetId = content.tweet_url ? getTweetId(content.tweet_url) : undefined;
  return (
    <div className="m-2 border p-4">
      {tweetId ? <Tweet id={tweetId} /> : <div>{content.content}</div>}
      {content.lat && content.lng && (
        <div className="h-[200px] w-full my-2">
          <Map
            initialViewState={{
              longitude: content.lng,
              latitude: content.lat,
              zoom: 8,
            }}
            style={{ width: "100%", height: "300px" }}
            mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
          >
            <Marker
              longitude={content.lng}
              latitude={content.lat}
              color="#FF0000"
            />
          </Map>
        </div>
      )}
      {content.ek_agent_url && (
        <div>
          <iframe
            src={content.ek_agent_url}
            className="w-full h-96 border-0"
            title="EK Agent View"
          />
        </div>
      )}
    </div>
  );
}

export default function Home() {
  const { data, error, isLoading } = useSWR<Content[]>(
    process.env.NEXT_PUBLIC_API_BASE_URL + "/content",
    fetcher
  );
  const [redText, setRedText] = useState("(1 new threat)");

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="w-1/2 mx-auto pt-10">
      <h1 className="text-2xl font-bold">
        Latest Threats<span className="text-red-500"> {redText}</span>
      </h1>
      <div className="flex flex-col gap-4">
        {data?.map((content) => (
          <ContentCard key={content.id} content={content} />
        ))}
      </div>
    </div>
  );
}
