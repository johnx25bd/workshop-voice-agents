# Run LiveKit locally

LiveKit Cloud handles the infrastructure for you, but LiveKit is fully open source and can be self-hosted. Running it locally gives you full control and works offline.

## With Docker

The quickest way to run LiveKit locally:

```bash
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  livekit/livekit-server --dev
```

This starts a LiveKit server in development mode with default credentials.

Update your `.env`:

```
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

## Without Docker

You can also install the LiveKit server binary directly. See the [self-hosting docs](https://docs.livekit.io/home/self-hosting/local/) for platform-specific instructions.

## Connecting the playground

The LiveKit Agents Playground can connect to your local server too. When prompted for a server URL, use `ws://localhost:7880` instead of your Cloud URL.

## When to self-host

- **Development** — faster iteration, no network round-trip to Cloud
- **Privacy** — audio never leaves your machine
- **Offline** — works without internet (though you'll still need API access for the AI models)
- **Production** — full control over infrastructure, scaling, and costs

For this workshop, Cloud is simpler. But knowing you can self-host is useful context for production deployments.
